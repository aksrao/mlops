
from pathlib import Path
import hashlib
import json

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data/raw/telco_customer_churn.csv"
ARTIFACT_DIR = ROOT / "artifacts"
ARTIFACT_DIR.mkdir(exist_ok=True)

NUMERIC = ["tenure", "MonthlyCharges", "TotalCharges"]
CATEGORICAL = [
    "Contract",
    "InternetService",
    "OnlineSecurity",
    "TechSupport",
    "PaymentMethod",
]
FEATURES = NUMERIC + CATEGORICAL

df = pd.read_csv(DATA_PATH)

# Convert whitespace and invalid numeric values to NaN.
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"].replace(r"^\s*$", float("nan"), regex=True),
    errors="coerce",
)

# Remove rows with a missing target and map labels to 0/1.
df = df.dropna(subset=["Churn"])
y = df["Churn"].map({"No": 0, "Yes": 1})

if y.isna().any():
    raise ValueError("Unexpected values in Churn target")

X = df[FEATURES].copy()
dataset_hash = hashlib.sha256(DATA_PATH.read_bytes()).hexdigest()

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore")),
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, NUMERIC),
    ("categorical", categorical_pipeline, CATEGORICAL),
])

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42,
    )),
])

# A local SQLite backend supports experiment tracking and model registry.
mlflow.set_tracking_uri(f"sqlite:///{ROOT / 'mlflow.db'}")
mlflow.set_experiment("telco-churn")

with mlflow.start_run() as run:
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions, zero_division=0),
        "recall": recall_score(y_test, predictions, zero_division=0),
        "f1": f1_score(y_test, predictions, zero_division=0),
        "roc_auc": roc_auc_score(y_test, probabilities),
    }

    mlflow.log_param("algorithm", "LogisticRegression")
    mlflow.log_param("random_state", 42)
    mlflow.log_param("class_weight", "balanced")
    mlflow.log_param("dataset_sha256", dataset_hash)
    mlflow.log_param("feature_columns", json.dumps(FEATURES))
    mlflow.log_metrics(metrics)

    model_path = ARTIFACT_DIR / "churn_model.joblib"
    joblib.dump(model, model_path)

    metadata = {
        "run_id": run.info.run_id,
        "dataset_sha256": dataset_hash,
        "features": FEATURES,
        "numeric_features": NUMERIC,
        "categorical_features": CATEGORICAL,
        "metrics": metrics,
    }

    (ARTIFACT_DIR / "metadata.json").write_text(
        json.dumps(metadata, indent=2)
    )

    mlflow.sklearn.log_model(
    model,
    name="model",
    serialization_format="pickle",
)

    print(json.dumps(metadata, indent=2))

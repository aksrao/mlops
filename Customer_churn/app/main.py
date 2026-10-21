
from pathlib import Path
import json

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "artifacts/churn_model.joblib"
METADATA_PATH = ROOT / "artifacts/metadata.json"

model = joblib.load(MODEL_PATH)
metadata = json.loads(METADATA_PATH.read_text())

app = FastAPI(title="Telco Churn Prediction API")


class ChurnRequest(BaseModel):
    tenure: int = Field(ge=0, le=100)
    monthly_charges: float = Field(ge=0)
    total_charges: float = Field(ge=0)
    contract: str
    internet_service: str
    online_security: str
    tech_support: str
    payment_method: str
import time

from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response

REQUESTS = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["endpoint"],
)


@app.middleware("http")
async def observe_requests(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)

    REQUESTS.labels(
        request.method,
        request.url.path,
        str(response.status_code),
    ).inc()

    LATENCY.labels(request.url.path).observe(
        time.perf_counter() - start
    )
    return response


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    return {
        "ready": model is not None,
        "model_run_id": metadata["run_id"],
    }


@app.post("/predict")
def predict(request: ChurnRequest):
    row = pd.DataFrame([{
        "tenure": request.tenure,
        "MonthlyCharges": request.monthly_charges,
        "TotalCharges": request.total_charges,
        "Contract": request.contract,
        "InternetService": request.internet_service,
        "OnlineSecurity": request.online_security,
        "TechSupport": request.tech_support,
        "PaymentMethod": request.payment_method,
    }])

    probability = float(model.predict_proba(row)[0][1])
    prediction = int(probability >= 0.5)

    return {
        "churn_prediction": "Yes" if prediction else "No",
        "churn_probability": probability,
        "model_run_id": metadata["run_id"],
        "dataset_sha256": metadata["dataset_sha256"],
    }

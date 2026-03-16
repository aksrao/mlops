from kfp import dsl
from kfp.dsl import Input, Output, Dataset, Model, Metrics, Artifact
from kfp import compiler

@dsl.component(
        base_image="python:3.10",
        packages_to_install=["pandas","scikit-learn","seaborn", "matplotlib"]
)
def load_data(dataset: Output[Dataset],plot_artifact: Output[Artifact]):
    from sklearn.datasets import load_iris
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df["target"] = iris.target

    df.to_csv(dataset.path, index=False)
    sns_plot = sns.pairplot(df, hue='target')
    
    # Save the figure to path Kubeflow expects
    fig_path = plot_artifact.path + ".png"
    sns_plot.savefig(fig_path)
    print("EDA plot saved at:", fig_path)

@dsl.component(
    base_image="python:3.10",
    packages_to_install=["pandas","scikit-learn","joblib"]
)
def train_model(dataset: Input[Dataset], model: Output[Model]):
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    import joblib
    df = pd.read_csv(dataset.path)

    X = df.drop("target", axis=1)
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    clf = LogisticRegression(max_iter=200)
    clf.fit(X_train, y_train)

    joblib.dump(clf, model.path)

@dsl.component(
    base_image="python:3.10",
    packages_to_install=["pandas", "scikit-learn", "joblib"]
)
def evaluate_model(
    dataset: Input[Dataset],
    model: Input[Model],
    metrics: Output[Metrics]
):
    import pandas as pd
    from sklearn.metrics import accuracy_score
    import joblib
    from sklearn.model_selection import train_test_split

    df = pd.read_csv(dataset.path)

    X = df.drop("target", axis=1)
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    clf = joblib.load(model.path)
    preds = clf.predict(X_test)

    acc = accuracy_score(y_test, preds)

    metrics.log_metric("accuracy", acc)
    print("Accuracy:", acc)
@dsl.pipeline(
    name="iris-classification-pipeline"
)
def iris_pipeline():

    data_task = load_data()

    train_task = train_model(
        dataset=data_task.outputs["dataset"]
    )

    evaluate_model(
        dataset=data_task.outputs["dataset"],
        model=train_task.outputs["model"]
    )
if __name__ == "__main__":
    compiler.Compiler().compile(iris_pipeline, 'iris_eda_model.yaml')
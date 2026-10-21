
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["ready"] is True


def test_prediction():
    payload = {
        "tenure": 12,
        "monthly_charges": 70.5,
        "total_charges": 846.0,
        "contract": "Month-to-month",
        "internet_service": "Fiber optic",
        "online_security": "No",
        "tech_support": "No",
        "payment_method": "Electronic check",
    }
    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    result = response.json()
    assert result["churn_prediction"] in ["Yes", "No"]
    assert 0 <= result["churn_probability"] <= 1


def test_invalid_tenure():
    response = client.post(
        "/predict",
        json={
            "tenure": -1,
            "monthly_charges": 70.5,
            "total_charges": 846.0,
            "contract": "Month-to-month",
            "internet_service": "Fiber optic",
            "online_security": "No",
            "tech_support": "No",
            "payment_method": "Electronic check",
        },
    )
    assert response.status_code == 422

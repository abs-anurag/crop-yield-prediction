from fastapi.testclient import TestClient

from backend.main import app
import backend.routes.predict as predict_route
import backend.services.prediction as prediction_service


client = TestClient(app)


VALID_PAYLOAD = {
    "crop": "Wheat",
    "area": 10,
    "rainfall": 500,
    "temperature": 25,
    "humidity": 60,
    "soil_type": "Loamy",
    "fertilizer": 100,
}


def test_health():
    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert "model_loaded" in data
    assert data["version"] == "1.0.0"


def test_metadata():
    response = client.get("/api/metadata")

    assert response.status_code == 200

    data = response.json()

    assert "supported_crops" in data
    assert "supported_soil_types" in data
    assert "feature_ranges" in data

    assert "Wheat" in data["supported_crops"]
    assert "Loamy" in data["supported_soil_types"]


def test_valid_prediction(monkeypatch):
    monkeypatch.setattr(
        predict_route,
        "get_prediction",
        lambda data: 42.5,
    )

    response = client.post("/api/predict", json=VALID_PAYLOAD)

    assert response.status_code == 200

    data = response.json()

    assert data["predicted_yield"] == 42.5
    assert data["unit"] == "tons/hectare"
    assert data["crop"] == "Wheat"


def test_missing_required_field():
    payload = VALID_PAYLOAD.copy()
    del payload["crop"]

    response = client.post("/api/predict", json=payload)

    assert response.status_code == 422


def test_invalid_type():
    payload = VALID_PAYLOAD.copy()
    payload["rainfall"] = "not-a-number"

    response = client.post("/api/predict", json=payload)

    assert response.status_code == 422


def test_invalid_range():
    payload = VALID_PAYLOAD.copy()
    payload["rainfall"] = 6000

    response = client.post("/api/predict", json=payload)

    assert response.status_code == 422


def test_model_unavailable(monkeypatch):
    monkeypatch.setattr(
        prediction_service,
        "is_model_loaded",
        lambda: False,
    )

    response = client.post("/api/predict", json=VALID_PAYLOAD)

    assert response.status_code == 503

    data = response.json()

    assert data["error"] == "MODEL_NOT_READY"
    assert (
        data["message"]
        == "ML model is not loaded. Please contact the administrator."
    )


def test_prediction_failure(monkeypatch):
    def failing_prediction(data):
        raise Exception("Prediction failed")

    monkeypatch.setattr(
        predict_route,
        "get_prediction",
        failing_prediction,
    )

    response = client.post("/api/predict", json=VALID_PAYLOAD)

    assert response.status_code == 500

    data = response.json()

    assert data["error"] == "PREDICTION_FAILED"
    assert (
        data["message"]
        == "An error occurred during prediction. Please try again."
    )
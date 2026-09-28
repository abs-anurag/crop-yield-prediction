"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import app


client = TestClient(app)


def test_health_endpoint():
    """Test GET /api/health returns correct structure."""
    response = client.get("/api/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "ok"
    assert "model_loaded" in data
    assert isinstance(data["model_loaded"], bool)
    assert data["version"] == "1.0.0"


def test_metadata_endpoint():
    """Test GET /api/metadata returns correct structure."""
    response = client.get("/api/metadata")
    assert response.status_code == 200
    
    data = response.json()
    assert "supported_crops" in data
    assert "supported_soil_types" in data
    assert "feature_ranges" in data
    
    # Check crops
    assert isinstance(data["supported_crops"], list)
    assert len(data["supported_crops"]) > 0
    assert "Wheat" in data["supported_crops"]
    
    # Check soil types
    assert isinstance(data["supported_soil_types"], list)
    assert len(data["supported_soil_types"]) > 0
    assert "Loamy" in data["supported_soil_types"]
    
    # Check feature ranges
    ranges = data["feature_ranges"]
    for feature in ["rainfall", "temperature", "humidity", "fertilizer", "area"]:
        assert feature in ranges
        assert "min" in ranges[feature]
        assert "max" in ranges[feature]
        assert "unit" in ranges[feature]


def test_predict_endpoint_valid():
    """Test POST /api/predict with valid input."""
    payload = {
        "crop": "Wheat",
        "area": 10.0,
        "rainfall": 600.0,
        "temperature": 25.0,
        "humidity": 65.0,
        "soil_type": "Loamy",
        "fertilizer": 100.0
    }
    
    response = client.post("/api/predict", json=payload)
    
    # May return 200 (if model loaded) or 503 (if model not loaded)
    assert response.status_code in [200, 503]
    
    if response.status_code == 200:
        data = response.json()
        assert "predicted_yield" in data
        assert isinstance(data["predicted_yield"], (int, float))
        assert data["unit"] == "tons/hectare"
        assert data["crop"] == "Wheat"


def test_predict_endpoint_invalid_crop():
    """Test POST /api/predict with invalid crop."""
    payload = {
        "crop": "InvalidCrop",
        "area": 10.0,
        "rainfall": 600.0,
        "temperature": 25.0,
        "humidity": 65.0,
        "soil_type": "Loamy",
        "fertilizer": 100.0
    }
    
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 422
    
    data = response.json()
    assert "detail" in data


def test_predict_endpoint_invalid_soil_type():
    """Test POST /api/predict with invalid soil type."""
    payload = {
        "crop": "Wheat",
        "area": 10.0,
        "rainfall": 600.0,
        "temperature": 25.0,
        "humidity": 65.0,
        "soil_type": "InvalidSoil",
        "fertilizer": 100.0
    }
    
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 422


def test_predict_endpoint_negative_area():
    """Test POST /api/predict with negative area."""
    payload = {
        "crop": "Wheat",
        "area": -1.0,
        "rainfall": 600.0,
        "temperature": 25.0,
        "humidity": 65.0,
        "soil_type": "Loamy",
        "fertilizer": 100.0
    }
    
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 422


def test_predict_endpoint_missing_required():
    """Test POST /api/predict with missing required field."""
    payload = {
        "crop": "Wheat",
        "area": 10.0,
        # missing rainfall, temperature, humidity, soil_type
    }
    
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 422


def test_predict_endpoint_out_of_range():
    """Test POST /api/predict with out-of-range values."""
    payload = {
        "crop": "Wheat",
        "area": 10.0,
        "rainfall": 6000.0,  # > 5000 max
        "temperature": 25.0,
        "humidity": 65.0,
        "soil_type": "Loamy",
        "fertilizer": 100.0
    }
    
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 422


def test_cors_headers():
    """Test CORS headers are present."""
    response = client.options("/api/health", headers={
        "Origin": "http://localhost:5173",
        "Access-Control-Request-Method": "GET"
    })
    
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
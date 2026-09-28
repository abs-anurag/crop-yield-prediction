"""
Integration and unit tests for the ML pipeline and prediction interface.
"""

from pathlib import Path
import numpy as np
import pytest
from ml.features import INPUT_FEATURES, SUPPORTED_CROPS, SUPPORTED_SOIL_TYPES
from ml.predict import predict_yield
from ml.train import run_training


def test_training_pipeline():
    results = run_training()

    assert Path(results["model_path"]).exists()
    assert Path(results["preprocessor_path"]).exists()
    assert results["rf_metrics"]["r2"] > 0.8
    assert results["selected_model"] in ["Random Forest", "Linear Regression"]


def test_predict_yield_wheat():
    sample_input = {
        "crop": "Wheat",
        "area": 10.0,
        "rainfall": 600.0,
        "temperature": 25.0,
        "humidity": 65.0,
        "soil_type": "Loamy",
        "fertilizer": 100.0,
    }

    predicted_yield = predict_yield(sample_input)

    assert isinstance(predicted_yield, float)
    assert predicted_yield > 0.0
    print(f"\n[Test Output] Predicted yield for Wheat: {predicted_yield} tons/ha")


def test_predict_yield_sugarcane():
    sample_input = {
        "crop": "Sugarcane",
        "area": 50.0,
        "rainfall": 1500.0,
        "temperature": 30.0,
        "humidity": 75.0,
        "soil_type": "Clay",
        "fertilizer": 250.0,
    }

    predicted_yield = predict_yield(sample_input)

    assert isinstance(predicted_yield, float)
    assert predicted_yield > 0.0
    print(f"\n[Test Output] Predicted yield for Sugarcane: {predicted_yield} tons/ha")


def test_predict_yield_missing_feature():
    invalid_input = {
        "crop": "Wheat",
        "area": 10.0,
        # missing rainfall
        "temperature": 25.0,
        "humidity": 65.0,
        "soil_type": "Loamy",
        "fertilizer": 100.0,
    }

    with pytest.raises(ValueError, match="Missing required input features"):
        predict_yield(invalid_input)

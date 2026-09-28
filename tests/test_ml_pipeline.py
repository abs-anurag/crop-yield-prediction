"""
Integration and unit tests for the ML pipeline and prediction interface based on real FAO & World Bank dataset.
"""

from pathlib import Path
import pytest
from ml.predict import predict_yield
from ml.train import run_training


def test_training_pipeline():
    results = run_training()

    assert Path(results["model_path"]).exists()
    assert Path(results["preprocessor_path"]).exists()
    assert results["rf_metrics"]["r2"] > 0.95
    assert results["selected_model"] == "Random Forest Regressor"


def test_predict_yield_exact_keys():
    sample_input = {
        "Area": "India",
        "Item": "Wheat",
        "Year": 2010,
        "average_rain_fall_mm_per_year": 1083.0,
        "pesticides_tonnes": 40000.0,
        "avg_temp": 24.5,
    }

    predicted_yield = predict_yield(sample_input)

    assert isinstance(predicted_yield, float)
    assert predicted_yield > 0.0
    print(f"\n[Test Output] Predicted yield for Wheat (India): {predicted_yield} tons/ha")


def test_predict_yield_alias_keys():
    sample_input = {
        "crop": "Maize",
        "country": "United States",
        "year": 2012,
        "rainfall": 1000.0,
        "pesticides": 150000.0,
        "temperature": 15.2,
    }

    predicted_yield = predict_yield(sample_input)

    assert isinstance(predicted_yield, float)
    assert predicted_yield > 0.0
    print(f"\n[Test Output] Predicted yield for Maize (United States): {predicted_yield} tons/ha")


def test_predict_yield_missing_feature():
    invalid_input = {
        "crop": "Wheat",
        "country": "India",
        # missing rainfall
        "temperature": 25.0,
        "pesticides": 100.0,
    }

    with pytest.raises(ValueError, match="Missing required input features"):
        predict_yield(invalid_input)

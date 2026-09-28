"""
Inference module for crop yield prediction based on real FAO & World Bank dataset metrics.
Exposes the predict_yield(input_dict) interface.
"""

from pathlib import Path
from typing import Any, Dict
import joblib
import pandas as pd
from ml.features import INPUT_FEATURES

# Module-level cache for model and preprocessor artifacts
_MODEL = None
_PREPROCESSOR = None

# Key alias mapping to accept both standard feature names and dataset column names
FEATURE_ALIASES = {
    "country": "Area",
    "area": "Area",
    "Area": "Area",

    "crop": "Item",
    "item": "Item",
    "Item": "Item",

    "year": "Year",
    "Year": "Year",

    "rainfall": "average_rain_fall_mm_per_year",
    "average_rain_fall_mm_per_year": "average_rain_fall_mm_per_year",

    "pesticides": "pesticides_tonnes",
    "pesticides_tonnes": "pesticides_tonnes",
    "fertilizer": "pesticides_tonnes",  # maps legacy fertilizer requests to pesticide input intensity

    "temperature": "avg_temp",
    "temp": "avg_temp",
    "avg_temp": "avg_temp",
}


def get_artifact_paths():
    project_root = Path(__file__).resolve().parent.parent
    model_path = project_root / "ml" / "model" / "crop_yield_model.joblib"
    preprocessor_path = project_root / "ml" / "model" / "preprocessor.joblib"
    return model_path, preprocessor_path


def load_artifacts(force_reload: bool = False):
    """Loads and caches the model and preprocessor artifacts."""
    global _MODEL, _PREPROCESSOR

    if _MODEL is None or _PREPROCESSOR is None or force_reload:
        model_path, preprocessor_path = get_artifact_paths()

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model artifact not found at {model_path}. Run ml/train.py first."
            )
        if not preprocessor_path.exists():
            raise FileNotFoundError(
                f"Preprocessor artifact not found at {preprocessor_path}. Run ml/train.py first."
            )

        _MODEL = joblib.load(model_path)
        _PREPROCESSOR = joblib.load(preprocessor_path)

    return _MODEL, _PREPROCESSOR


def normalize_input_dict(input_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Maps incoming dict keys (aliases or exact names) to exact model INPUT_FEATURES."""
    normalized = {}
    for raw_key, value in input_dict.items():
        canonical_key = FEATURE_ALIASES.get(raw_key, raw_key)
        normalized[canonical_key] = value

    missing = [feature for feature in INPUT_FEATURES if feature not in normalized]
    if missing:
        raise ValueError(f"Missing required input features: {missing}. Provided keys: {list(input_dict.keys())}")

    return normalized


def predict_yield(input_dict: Dict[str, Any]) -> float:
    """
    Accepts an input dictionary containing crop yield parameters and returns the predicted yield in tons/hectare.

    Expected input_dict keys (or supported aliases):
        - Area / country / area (str): e.g., "India", "United States", "Albania"
        - Item / crop (str): e.g., "Wheat", "Maize", "Rice, paddy", "Potatoes", "Soybeans"
        - Year / year (int): e.g., 2010
        - average_rain_fall_mm_per_year / rainfall (float): annual precipitation in mm
        - pesticides_tonnes / pesticides / fertilizer (float): pesticide usage in tonnes
        - avg_temp / temperature (float): average temperature in °C

    Returns:
        float: Predicted crop yield in metric tons per hectare.
    """
    # 1. Normalize input features
    norm_dict = normalize_input_dict(input_dict)

    # 2. Build DataFrame with exact feature ordering
    input_df = pd.DataFrame([{feature: norm_dict[feature] for feature in INPUT_FEATURES}])

    # 3. Load model and preprocessor
    model, preprocessor = load_artifacts()

    # 4. Transform input
    transformed_input = preprocessor.transform(input_df)

    # 5. Predict
    prediction = model.predict(transformed_input)

    # 6. Extract float yield in tons/ha
    predicted_val = float(prediction[0])
    return round(predicted_val, 2)

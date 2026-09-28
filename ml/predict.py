"""
Inference module for crop yield prediction.
Provides the predict_yield(input_dict) interface required by the Backend API.
"""

from pathlib import Path
from typing import Any, Dict
import joblib
import pandas as pd
from ml.features import INPUT_FEATURES

# Module-level cache for model and preprocessor artifacts
_MODEL = None
_PREPROCESSOR = None


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


def predict_yield(input_dict: Dict[str, Any]) -> float:
    """
    Accepts an input dictionary containing crop yield features and returns the predicted yield (float).

    Expected input_dict keys:
        - crop (str): e.g. "Wheat", "Rice", "Maize", "Cotton", "Sugarcane"
        - area (float): in hectares
        - rainfall (float): in mm
        - temperature (float): in °C
        - humidity (float): in %
        - soil_type (str): e.g. "Loamy", "Sandy", "Clay", "Silt", "Peaty"
        - fertilizer (float): in kg/ha

    Returns:
        float: Predicted yield in tons/hectare.
    """
    # 1. Validate required input keys
    missing_keys = [key for key in INPUT_FEATURES if key not in input_dict]
    if missing_keys:
        raise ValueError(f"Missing required input features: {missing_keys}")

    # 2. Convert input dict to DataFrame with expected feature ordering
    input_df = pd.DataFrame([{feature: input_dict[feature] for feature in INPUT_FEATURES}])

    # 3. Load model and preprocessor
    model, preprocessor = load_artifacts()

    # 4. Transform input
    transformed_input = preprocessor.transform(input_df)

    # 5. Predict
    prediction = model.predict(transformed_input)

    # 6. Extract float value
    predicted_val = float(prediction[0])
    return round(predicted_val, 2)

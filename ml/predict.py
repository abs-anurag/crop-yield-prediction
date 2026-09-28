"""Prediction interface for crop yield prediction."""

import joblib
import pandas as pd
import numpy as np
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.features import FEATURE_COLUMNS


# Global model state (loaded once)
_model = None
_preprocessor = None


def load_artifacts(model_path: str = "ml/model/crop_yield_model.joblib",
                   preprocessor_path: str = "ml/model/preprocessor.joblib"):
    """Load model and preprocessor artifacts."""
    global _model, _preprocessor
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found: {model_path}")
    if not os.path.exists(preprocessor_path):
        raise FileNotFoundError(f"Preprocessor not found: {preprocessor_path}")
    
    _model = joblib.load(model_path)
    _preprocessor = joblib.load(preprocessor_path)
    
    return _model, _preprocessor


def predict_yield(input_dict: dict) -> float:
    """
    Predict crop yield from input parameters.
    
    Args:
        input_dict: Dictionary with keys:
            - crop: str (e.g., "Wheat")
            - area: float (hectares)
            - rainfall: float (mm)
            - temperature: float (°C)
            - humidity: float (%)
            - soil_type: str (e.g., "Loamy")
            - fertilizer: float (kg/ha, optional, default 0)
    
    Returns:
        Predicted yield in tons/hectare (float)
    
    Raises:
        ValueError: If input validation fails
        RuntimeError: If model not loaded
    """
    global _model, _preprocessor
    
    # Load artifacts if not already loaded
    if _model is None or _preprocessor is None:
        load_artifacts()
    
    # Validate required fields
    required_fields = ['crop', 'area', 'rainfall', 'temperature', 'humidity', 'soil_type']
    for field in required_fields:
        if field not in input_dict:
            raise ValueError(f"Missing required field: {field}")
    
    # Set default for optional field
    if 'fertilizer' not in input_dict:
        input_dict['fertilizer'] = 0.0
    
    # Create DataFrame with correct column order
    df = pd.DataFrame([input_dict])[FEATURE_COLUMNS]
    
    # Apply preprocessing (SAME as training - no refitting!)
    X = _preprocessor.transform(df)
    
    # Predict
    prediction = _model.predict(X)[0]
    
    return float(prediction)


def predict_yield_batch(input_list: list) -> list:
    """
    Predict yield for multiple inputs.
    
    Args:
        input_list: List of input dictionaries
    
    Returns:
        List of predicted yields (floats)
    """
    return [predict_yield(inp) for inp in input_list]


# TEMPORARY MOCK for Day 1 development
# REMOVE before final demo
def _mock_predict_yield(input_dict: dict) -> float:
    """TEMPORARY MOCK - Replace with real model."""
    print(f"[MOCK] predict_yield called with: {input_dict}")
    return 42.5


# For Day 1 development, uncomment the mock:
# predict_yield = _mock_predict_yield
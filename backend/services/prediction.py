"""Prediction service - loads model and calls ML predict_yield()."""

import os
from backend.config import get_settings


# Global model state
_model = None
_preprocessor = None
_model_loaded = False


def load_model_artifacts() -> bool:
    """Load model and preprocessor artifacts at startup."""
    global _model, _preprocessor, _model_loaded
    
    settings = get_settings()
    
    try:
        import joblib
        
        if not os.path.exists(settings.MODEL_PATH):
            print(f"Model file not found: {settings.MODEL_PATH}")
            return False
        
        if not os.path.exists(settings.PREPROCESSOR_PATH):
            print(f"Preprocessor file not found: {settings.PREPROCESSOR_PATH}")
            return False
        
        _model = joblib.load(settings.MODEL_PATH)
        _preprocessor = joblib.load(settings.PREPROCESSOR_PATH)
        _model_loaded = True
        print("Model artifacts loaded successfully")
        return True
    
    except Exception as e:
        print(f"Failed to load model artifacts: {e}")
        _model_loaded = False
        return False


def is_model_loaded() -> bool:
    """Check if model is loaded."""
    return _model_loaded


def get_prediction(request_data: dict) -> float:
    """
    Get prediction from ML model.
    
    MOCK for Day 1 - Replace with real model integration after Checkpoint 1.
    """
    # TODO: Replace with real model integration
    # from ml.predict import predict_yield
    # return predict_yield(request_data)
    
    # TEMPORARY MOCK - Remove before final demo
    print(f"[MOCK] Prediction requested for: {request_data}")
    return 42.5


def get_model_info() -> dict:
    """Get model information for debugging."""
    return {
        "model_loaded": _model_loaded,
        "model_path": get_settings().MODEL_PATH,
        "preprocessor_path": get_settings().PREPROCESSOR_PATH,
    }
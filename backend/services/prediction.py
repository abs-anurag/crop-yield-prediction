from pathlib import Path
from typing import Any

from backend.config import MODEL_PATH, PREPROCESSOR_PATH


def is_model_loaded() -> bool:
    """
    The model is considered ready only when both required artifacts exist.
    """
    return Path(MODEL_PATH).is_file() and Path(PREPROCESSOR_PATH).is_file()


def get_prediction(request_data: dict[str, Any]) -> float:
    """
    Delegate prediction to the ML layer.

    The backend must not duplicate preprocessing or feature engineering.
    """
    if not is_model_loaded():
        raise RuntimeError("MODEL_NOT_READY")

    from ml.predict import predict_yield

    prediction = predict_yield(request_data)

    return float(prediction)
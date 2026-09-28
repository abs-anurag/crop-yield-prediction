"""
Model evaluation functions for calculating MAE, RMSE, and R2 metrics on real dataset.
"""

from typing import Dict
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Evaluates model predictions against ground truth target values.

    Returns dictionary containing MAE, RMSE, and R2 metrics.
    """
    mae = float(mean_absolute_error(y_true, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    r2 = float(r2_score(y_true, y_pred))

    return {
        "mae": round(mae, 4),
        "rmse": round(rmse, 4),
        "r2": round(r2, 4),
    }


def print_evaluation_summary(model_name: str, metrics: Dict[str, float], unit: str = "tons/ha") -> None:
    """Prints formatted evaluation metrics summary."""
    print(f"--- Evaluation Metrics for {model_name} ---")
    print(f"MAE  : {metrics['mae']:.4f} {unit}")
    print(f"RMSE : {metrics['rmse']:.4f} {unit}")
    print(f"R²   : {metrics['r2']:.4f}")
    print("-" * (32 + len(model_name)))

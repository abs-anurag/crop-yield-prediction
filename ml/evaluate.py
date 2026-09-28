"""Evaluation metrics for crop yield prediction models."""

import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def evaluate_model(model, X_test, y_test) -> dict:
    """
    Evaluate model on test set.
    
    Returns:
        dict with keys: rmse, mae, r2
    """
    y_pred = model.predict(X_test)
    
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    return {
        "rmse": float(rmse),
        "mae": float(mae),
        "r2": float(r2),
    }


def print_evaluation(metrics: dict, model_name: str = "Model"):
    """Print formatted evaluation metrics."""
    print(f"\n{model_name} Evaluation:")
    print(f"  RMSE: {metrics['rmse']:.4f}")
    print(f"  MAE:  {metrics['mae']:.4f}")
    print(f"  R²:   {metrics['r2']:.4f}")


def compare_models(baseline_metrics: dict, primary_metrics: dict):
    """Compare baseline and primary model metrics."""
    print("\nModel Comparison:")
    print(f"{'Metric':<10} {'Baseline':>12} {'Primary':>12} {'Improvement':>12}")
    print("-" * 46)
    
    for metric in ['rmse', 'mae', 'r2']:
        baseline = baseline_metrics[metric]
        primary = primary_metrics[metric]
        
        if metric in ['rmse', 'mae']:
            # Lower is better
            improvement = ((baseline - primary) / baseline) * 100
            better = "↓" if primary < baseline else "↑"
        else:
            # Higher is better
            improvement = ((primary - baseline) / baseline) * 100
            better = "↑" if primary > baseline else "↓"
        
        print(f"{metric.upper():<10} {baseline:>12.4f} {primary:>12.4f} {improvement:>+11.1f}% {better}")
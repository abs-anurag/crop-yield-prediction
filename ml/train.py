"""
Training script for Crop Yield Prediction ML models.
Loads data, fits preprocessing pipeline, trains Linear Regression and Random Forest models,
evaluates metrics, selects the best performing model, and saves artifacts.
"""

import os
from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from ml.evaluate import evaluate_model, print_evaluation_summary
from ml.features import INPUT_FEATURES, TARGET_VARIABLE
from ml.preprocessing import create_preprocessor


def run_training():
    project_root = Path(__file__).resolve().parent.parent
    data_path = project_root / "data" / "raw" / "crop_yield.csv"
    model_dir = project_root / "ml" / "model"
    model_dir.mkdir(parents=True, exist_ok=True)

    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found at {data_path}")

    print(f"Loading dataset from {data_path}...")
    df = pd.read_csv(data_path)

    X = df[INPUT_FEATURES]
    y = df[TARGET_VARIABLE]

    # Train / Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"Train samples: {len(X_train)}, Test samples: {len(X_test)}")

    # Fit preprocessor on training set
    preprocessor = create_preprocessor()
    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc = preprocessor.transform(X_test)

    # 1. Train Linear Regression (Baseline)
    print("\nTraining Linear Regression (Baseline)...")
    lr_model = LinearRegression()
    lr_model.fit(X_train_proc, y_train)
    y_pred_lr = lr_model.predict(X_test_proc)
    lr_metrics = evaluate_model(y_test.values, y_pred_lr)
    print_evaluation_summary("Linear Regression", lr_metrics)

    # 2. Train Random Forest Regressor (Primary)
    print("\nTraining Random Forest Regressor...")
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train_proc, y_train)
    y_pred_rf = rf_model.predict(X_test_proc)
    rf_metrics = evaluate_model(y_test.values, y_pred_rf)
    print_evaluation_summary("Random Forest", rf_metrics)

    # Model Selection based on R² score (or lower RMSE)
    if rf_metrics["r2"] >= lr_metrics["r2"]:
        best_model_name = "Random Forest"
        best_model = rf_model
        best_metrics = rf_metrics
    else:
        best_model_name = "Linear Regression"
        best_model = lr_model
        best_metrics = lr_metrics

    print(
        f"\nSelected Model: {best_model_name} (R² = {best_metrics['r2']:.4f}, RMSE = {best_metrics['rmse']:.4f})"
    )

    # Save artifacts
    model_path = model_dir / "crop_yield_model.joblib"
    preprocessor_path = model_dir / "preprocessor.joblib"

    joblib.dump(best_model, model_path)
    joblib.dump(preprocessor, preprocessor_path)

    print(f"Saved model artifact to: {model_path}")
    print(f"Saved preprocessor artifact to: {preprocessor_path}")

    return {
        "lr_metrics": lr_metrics,
        "rf_metrics": rf_metrics,
        "selected_model": best_model_name,
        "model_path": str(model_path),
        "preprocessor_path": str(preprocessor_path),
    }


if __name__ == "__main__":
    run_training()

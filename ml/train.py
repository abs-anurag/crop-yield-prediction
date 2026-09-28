"""Training script for crop yield prediction models."""

import pandas as pd
import numpy as np
import joblib
import os
import sys

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.preprocessing import PreprocessingPipeline
from ml.features import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    RANDOM_STATE,
    RF_N_ESTIMATORS,
)
from ml.evaluate import evaluate_model


def load_data(data_path: str = "data/raw/crop_yield.csv") -> pd.DataFrame:
    """Load raw dataset."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")
    return pd.read_csv(data_path)


def train_baseline_model(X_train, y_train):
    """Train Linear Regression baseline model."""
    from sklearn.linear_model import LinearRegression
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def train_primary_model(X_train, y_train):
    """Train Random Forest primary model."""
    from sklearn.ensemble import RandomForestRegressor
    from ml.features import (
        RF_MAX_DEPTH,
        RF_MIN_SAMPLES_SPLIT,
        RF_MIN_SAMPLES_LEAF,
    )
    
    model = RandomForestRegressor(
        n_estimators=RF_N_ESTIMATORS,
        max_depth=RF_MAX_DEPTH,
        min_samples_split=RF_MIN_SAMPLES_SPLIT,
        min_samples_leaf=RF_MIN_SAMPLES_LEAF,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    return model


def save_artifacts(model, preprocessor, model_dir: str = "ml/model"):
    """Save model and preprocessor artifacts."""
    os.makedirs(model_dir, exist_ok=True)
    
    model_path = os.path.join(model_dir, "crop_yield_model.joblib")
    preprocessor_path = os.path.join(model_dir, "preprocessor.joblib")
    
    joblib.dump(model, model_path)
    joblib.dump(preprocessor, preprocessor_path)
    
    print(f"Model saved to: {model_path}")
    print(f"Preprocessor saved to: {preprocessor_path}")
    
    return model_path, preprocessor_path


def main():
    """Main training pipeline."""
    print("=" * 60)
    print("Crop Yield Prediction - Model Training")
    print("=" * 60)
    
    # 1. Load data
    print("\n[1/6] Loading dataset...")
    df = load_data()
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # 2. Create preprocessing pipeline
    print("\n[2/6] Creating preprocessing pipeline...")
    pipeline = PreprocessingPipeline()
    
    # 3. Prepare train/test split
    print("\n[3/6] Preparing train/test split...")
    X_train, X_test, y_train, y_test = pipeline.prepare_data(df)
    print(f"Train shape: {X_train.shape}, Test shape: {X_test.shape}")
    
    # 4. Train baseline model
    print("\n[4/6] Training baseline (Linear Regression)...")
    baseline_model = train_baseline_model(X_train, y_train)
    baseline_metrics = evaluate_model(baseline_model, X_test, y_test)
    print(f"Baseline - RMSE: {baseline_metrics['rmse']:.4f}, "
          f"MAE: {baseline_metrics['mae']:.4f}, R²: {baseline_metrics['r2']:.4f}")
    
    # 5. Train primary model
    print("\n[5/6] Training primary (Random Forest)...")
    primary_model = train_primary_model(X_train, y_train)
    primary_metrics = evaluate_model(primary_model, X_test, y_test)
    print(f"Primary - RMSE: {primary_metrics['rmse']:.4f}, "
          f"MAE: {primary_metrics['mae']:.4f}, R²: {primary_metrics['r2']:.4f}")
    
    # 6. Save artifacts
    print("\n[6/6] Saving model artifacts...")
    save_artifacts(primary_model, pipeline)
    
    print("\n" + "=" * 60)
    print("Training complete!")
    print("=" * 60)
    print(f"\nBaseline (Linear Regression):")
    print(f"  RMSE: {baseline_metrics['rmse']:.4f}")
    print(f"  MAE:  {baseline_metrics['mae']:.4f}")
    print(f"  R²:   {baseline_metrics['r2']:.4f}")
    print(f"\nPrimary (Random Forest):")
    print(f"  RMSE: {primary_metrics['rmse']:.4f}")
    print(f"  MAE:  {primary_metrics['mae']:.4f}")
    print(f"  R²:   {primary_metrics['r2']:.4f}")
    print("\nArtifacts saved to ml/model/")
    print("Next steps:")
    print("  1. Copy ml/model/*.joblib to backend/ml/model/")
    print("  2. Update backend/services/prediction.py to use real model")
    print("  3. Run backend and test /api/predict")


if __name__ == "__main__":
    main()
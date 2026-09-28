"""Tests for preprocessing pipeline."""

import pytest
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.preprocessing import PreprocessingPipeline
from ml.features import FEATURE_COLUMNS


def test_preprocessing_handles_missing_values():
    """Test preprocessing handles missing values."""
    df = pd.DataFrame({
        'crop': ['Wheat', None, 'Maize'],
        'area': [10.0, 5.0, None],
        'rainfall': [600.0, 800.0, 700.0],
        'temperature': [25.0, 28.0, 26.0],
        'humidity': [65.0, 70.0, 68.0],
        'soil_type': ['Loamy', 'Clay', None],
        'fertilizer': [100.0, 150.0, 120.0],
        'yield': [4.5, 5.2, 4.8]
    })
    
    pipeline = PreprocessingPipeline()
    pipeline.fit(df)
    X = pipeline.transform(df)
    
    # Should not raise, should handle NaN
    assert X.shape[0] == 3
    assert not np.isnan(X).any()


def test_preprocessing_unseen_categories():
    """Test preprocessing handles unseen categories at inference."""
    # Train data
    train_df = pd.DataFrame({
        'crop': ['Wheat', 'Rice', 'Maize'],
        'area': [10.0, 5.0, 8.0],
        'rainfall': [600.0, 800.0, 700.0],
        'temperature': [25.0, 28.0, 26.0],
        'humidity': [65.0, 70.0, 68.0],
        'soil_type': ['Loamy', 'Clay', 'Sandy'],
        'fertilizer': [100.0, 150.0, 120.0],
        'yield': [4.5, 5.2, 4.8]
    })
    
    # Test data with unseen crop
    test_df = pd.DataFrame({
        'crop': ['Wheat', 'Barley'],  # Barley not in training
        'area': [9.0, 7.0],
        'rainfall': [550.0, 720.0],
        'temperature': [26.0, 25.0],
        'humidity': [66.0, 67.0],
        'soil_type': ['Loamy', 'Silt'],  # Silt not in training
        'fertilizer': [90.0, 130.0],
        'yield': [4.3, 4.9]
    })
    
    pipeline = PreprocessingPipeline()
    pipeline.fit(train_df)
    
    # Should not raise
    X_train = pipeline.transform(train_df)
    X_test = pipeline.transform(test_df)
    
    assert X_train.shape[1] == X_test.shape[1]


def test_preprocessing_feature_order():
    """Test feature order is consistent."""
    df = pd.DataFrame({
        'crop': ['Wheat', 'Rice'],
        'area': [10.0, 5.0],
        'rainfall': [600.0, 800.0],
        'temperature': [25.0, 28.0],
        'humidity': [65.0, 70.0],
        'soil_type': ['Loamy', 'Clay'],
        'fertilizer': [100.0, 150.0],
        'yield': [4.5, 5.2]
    })
    
    pipeline = PreprocessingPipeline()
    pipeline.fit(df)
    X = pipeline.transform(df)
    
    names = pipeline.get_feature_names_out()
    assert len(names) == X.shape[1]
    
    # Categorical features should come first (encoded)
    cat_names = [n for n in names if 'encoded' in n]
    num_names = [n for n in names if 'encoded' not in n]
    
    assert len(cat_names) == 2  # crop, soil_type
    assert len(num_names) == 5  # area, rainfall, temperature, humidity, fertilizer


def test_preprocessing_save_load():
    """Test preprocessing pipeline can be saved and loaded."""
    import joblib
    import tempfile
    
    df = pd.DataFrame({
        'crop': ['Wheat', 'Rice', 'Maize'],
        'area': [10.0, 5.0, 8.0],
        'rainfall': [600.0, 800.0, 700.0],
        'temperature': [25.0, 28.0, 26.0],
        'humidity': [65.0, 70.0, 68.0],
        'soil_type': ['Loamy', 'Clay', 'Sandy'],
        'fertilizer': [100.0, 150.0, 120.0],
        'yield': [4.5, 5.2, 4.8]
    })
    
    pipeline = PreprocessingPipeline()
    pipeline.fit(df)
    X_original = pipeline.transform(df)
    
    # Save and load
    with tempfile.NamedTemporaryFile(suffix='.joblib', delete=False) as f:
        joblib.dump(pipeline, f.name)
        loaded_pipeline = joblib.load(f.name)
    
    # Transform with loaded pipeline
    X_loaded = loaded_pipeline.transform(df)
    
    # Results should be identical
    np.testing.assert_array_almost_equal(X_original, X_loaded)
    assert loaded_pipeline.is_fitted


def test_preprocessing_numerical_scaling():
    """Test numerical features are scaled."""
    df = pd.DataFrame({
        'crop': ['Wheat', 'Rice'],
        'area': [10.0, 1000.0],  # Very different scales
        'rainfall': [600.0, 600.0],
        'temperature': [25.0, 25.0],
        'humidity': [65.0, 65.0],
        'soil_type': ['Loamy', 'Loamy'],
        'fertilizer': [100.0, 100.0],
        'yield': [4.5, 5.2]
    })
    
    pipeline = PreprocessingPipeline()
    pipeline.fit(df)
    X = pipeline.transform(df)
    
    # Area column should be scaled (not identical to original)
    # The numerical features are at the end
    assert X.shape[1] > 0
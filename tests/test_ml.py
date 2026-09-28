"""Tests for ML module."""

import pytest
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.features import FEATURE_COLUMNS, CATEGORICAL_FEATURES, NUMERICAL_FEATURES
from ml.preprocessing import PreprocessingPipeline


def test_feature_columns():
    """Test feature column definitions."""
    assert 'crop' in FEATURE_COLUMNS
    assert 'area' in FEATURE_COLUMNS
    assert 'rainfall' in FEATURE_COLUMNS
    assert 'temperature' in FEATURE_COLUMNS
    assert 'humidity' in FEATURE_COLUMNS
    assert 'soil_type' in FEATURE_COLUMNS
    assert 'fertilizer' in FEATURE_COLUMNS
    assert len(FEATURE_COLUMNS) == 7


def test_categorical_features():
    """Test categorical feature definitions."""
    assert 'crop' in CATEGORICAL_FEATURES
    assert 'soil_type' in CATEGORICAL_FEATURES
    assert len(CATEGORICAL_FEATURES) == 2


def test_numerical_features():
    """Test numerical feature definitions."""
    assert 'area' in NUMERICAL_FEATURES
    assert 'rainfall' in NUMERICAL_FEATURES
    assert 'temperature' in NUMERICAL_FEATURES
    assert 'humidity' in NUMERICAL_FEATURES
    assert 'fertilizer' in NUMERICAL_FEATURES
    assert len(NUMERICAL_FEATURES) == 5


def test_preprocessing_pipeline():
    """Test preprocessing pipeline fit/transform."""
    # Create sample data
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
    
    # Transform
    X = pipeline.transform(df)
    assert X.shape[0] == 3
    assert X.shape[1] > 0
    assert pipeline.is_fitted


def test_preprocessing_consistency():
    """Test train/serve consistency."""
    # Training data
    train_df = pd.DataFrame({
        'crop': ['Wheat', 'Rice', 'Maize', 'Wheat', 'Rice'],
        'area': [10.0, 5.0, 8.0, 12.0, 6.0],
        'rainfall': [600.0, 800.0, 700.0, 650.0, 750.0],
        'temperature': [25.0, 28.0, 26.0, 24.0, 27.0],
        'humidity': [65.0, 70.0, 68.0, 63.0, 69.0],
        'soil_type': ['Loamy', 'Clay', 'Sandy', 'Loamy', 'Clay'],
        'fertilizer': [100.0, 150.0, 120.0, 110.0, 140.0],
        'yield': [4.5, 5.2, 4.8, 4.7, 5.0]
    })
    
    # Test data (new samples)
    test_df = pd.DataFrame({
        'crop': ['Wheat', 'Maize'],
        'area': [9.0, 7.0],
        'rainfall': [550.0, 720.0],
        'temperature': [26.0, 25.0],
        'humidity': [66.0, 67.0],
        'soil_type': ['Sandy', 'Loamy'],
        'fertilizer': [90.0, 130.0],
        'yield': [4.3, 4.9]
    })
    
    # Fit on train
    pipeline = PreprocessingPipeline()
    pipeline.fit(train_df)
    
    # Transform both
    X_train = pipeline.transform(train_df)
    X_test = pipeline.transform(test_df)
    
    # Same number of features
    assert X_train.shape[1] == X_test.shape[1]
    
    # Feature names consistent
    names = pipeline.get_feature_names_out()
    assert len(names) == X_train.shape[1]


def test_mock_predict_yield():
    """Test mock prediction function."""
    from ml.predict import _mock_predict_yield
    
    result = _mock_predict_yield({
        'crop': 'Wheat',
        'area': 10.0,
        'rainfall': 600.0,
        'temperature': 25.0,
        'humidity': 65.0,
        'soil_type': 'Loamy',
        'fertilizer': 100.0
    })
    
    assert result == 42.5
    assert isinstance(result, float)
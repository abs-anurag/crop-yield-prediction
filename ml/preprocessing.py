"""Preprocessing pipeline for crop yield prediction."""

import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from ml.features import (
    CATEGORICAL_FEATURES,
    NUMERICAL_FEATURES,
    FEATURE_COLUMNS,
    TARGET_COLUMN,
)


class PreprocessingPipeline(BaseEstimator, TransformerMixin):
    """
    Complete preprocessing pipeline for crop yield data.
    
    Handles:
    - Missing value imputation
    - Categorical encoding (LabelEncoder)
    - Numerical scaling (StandardScaler)
    - Feature selection
    
    IMPORTANT: This pipeline MUST be saved with joblib and loaded
    for inference to ensure train/serve consistency.
    """
    
    def __init__(self):
        self.categorical_features = CATEGORICAL_FEATURES
        self.numerical_features = NUMERICAL_FEATURES
        self.feature_columns = FEATURE_COLUMNS
        self.target_column = TARGET_COLUMN
        
        # Encoders and scalers (fitted during fit())
        self.categorical_encoders = {}
        self.numerical_scaler = None
        self.column_transformer = None
        self.is_fitted = False
    
    def fit(self, X: pd.DataFrame, y=None):
        """Fit the preprocessing pipeline on training data."""
        X = X.copy()
        
        # Ensure all feature columns exist
        for col in self.feature_columns:
            if col not in X.columns:
                raise ValueError(f"Missing feature column: {col}")
        
        # Fit categorical encoders
        for col in self.categorical_features:
            if col in X.columns:
                encoder = LabelEncoder()
                # Handle unseen categories by adding 'Unknown'
                X[col] = X[col].fillna('Unknown').astype(str)
                encoder.fit(X[col])
                self.categorical_encoders[col] = encoder
        
        # Fit numerical scaler
        if self.numerical_features:
            self.numerical_scaler = StandardScaler()
            X_num = X[self.numerical_features].fillna(0)
            self.numerical_scaler.fit(X_num)
        
        # Create column transformer for consistent transform
        transformers = []
        
        if self.categorical_features:
            # Use a simple passthrough since we handle encoding manually
            transformers.append(('cat', 'passthrough', self.categorical_features))
        
        if self.numerical_features:
            transformers.append(('num', 'passthrough', self.numerical_features))
        
        self.is_fitted = True
        return self
    
    def transform(self, X: pd.DataFrame) -> np.ndarray:
        """Transform data using fitted pipeline."""
        if not self.is_fitted:
            raise ValueError("Pipeline not fitted. Call fit() first.")
        
        X = X.copy()
        
        # Ensure all feature columns exist
        for col in self.feature_columns:
            if col not in X.columns:
                raise ValueError(f"Missing feature column: {col}")
        
        # Encode categorical features
        encoded_features = []
        
        for col in self.categorical_features:
            if col in X.columns:
                encoder = self.categorical_encoders[col]
                # Handle unseen categories
                X[col] = X[col].fillna('Unknown').astype(str)
                # Transform, replacing unseen with first class
                known_classes = set(encoder.classes_)
                X[col] = X[col].apply(
                    lambda x: x if x in known_classes else encoder.classes_[0]
                )
                encoded = encoder.transform(X[col])
                encoded_features.append(encoded.reshape(-1, 1))
        
        # Scale numerical features
        if self.numerical_features and self.numerical_scaler:
            X_num = X[self.numerical_features].fillna(0)
            scaled = self.numerical_scaler.transform(X_num)
            encoded_features.append(scaled)
        
        # Combine all features
        if encoded_features:
            return np.hstack(encoded_features)
        else:
            return np.array([]).reshape(len(X), 0)
    
    def fit_transform(self, X: pd.DataFrame, y=None) -> np.ndarray:
        """Fit and transform in one step."""
        return self.fit(X, y).transform(X)
    
    def prepare_data(self, df: pd.DataFrame):
        """Prepare train/test split from raw dataframe."""
        from sklearn.model_selection import train_test_split
        
        # Select features and target
        X = df[self.feature_columns].copy()
        y = df[self.target_column].copy()
        
        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Fit on train, transform both
        self.fit(X_train, y_train)
        X_train_transformed = self.transform(X_train)
        X_test_transformed = self.transform(X_test)
        
        return X_train_transformed, X_test_transformed, y_train, y_test
    
    def get_feature_names_out(self):
        """Get output feature names after transformation."""
        names = []
        for col in self.categorical_features:
            if col in self.categorical_encoders:
                names.append(f"{col}_encoded")
        names.extend(self.numerical_features)
        return np.array(names)


def create_preprocessing_pipeline() -> PreprocessingPipeline:
    """Factory function to create a new preprocessing pipeline."""
    return PreprocessingPipeline()
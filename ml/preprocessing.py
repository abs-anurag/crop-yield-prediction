"""
Preprocessing pipeline construction for Crop Yield Prediction ML pipeline.
"""

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from ml.features import CATEGORICAL_FEATURES, NUMERICAL_FEATURES


def create_preprocessor() -> ColumnTransformer:
    """
    Creates and returns an unfitted Scikit-Learn ColumnTransformer pipeline.

    Categorical features: One-Hot Encoded (handle_unknown='ignore')
    Numerical features: Standard Scaled
    """
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                CATEGORICAL_FEATURES,
            ),
            ("num", StandardScaler(), NUMERICAL_FEATURES),
        ],
        remainder="drop",
    )
    return preprocessor

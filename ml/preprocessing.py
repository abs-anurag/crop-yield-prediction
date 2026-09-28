"""
Preprocessing pipeline construction for Crop Yield Prediction ML pipeline using real dataset features.
"""

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from ml.features import CATEGORICAL_FEATURES, NUMERICAL_FEATURES


def create_preprocessor() -> ColumnTransformer:
    """
    Creates and returns an unfitted Scikit-Learn ColumnTransformer pipeline.

    Categorical features ('Area', 'Item'): One-Hot Encoded (handle_unknown='ignore')
    Numerical features ('Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp'): Standard Scaled
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

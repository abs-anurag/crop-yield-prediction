"""
Authoritative feature definitions and schema constants for the Crop Yield Prediction ML pipeline.
"""

# Feature Groups
CATEGORICAL_FEATURES = ["crop", "soil_type"]
NUMERICAL_FEATURES = ["area", "rainfall", "temperature", "humidity", "fertilizer"]

# All Input Features
INPUT_FEATURES = CATEGORICAL_FEATURES + NUMERICAL_FEATURES

# Target Variable
TARGET_VARIABLE = "yield"

# Units & Display Metadata
TARGET_UNIT = "tons/hectare"

# Valid Categories (derived from dataset)
SUPPORTED_CROPS = ["Wheat", "Rice", "Maize", "Cotton", "Sugarcane"]
SUPPORTED_SOIL_TYPES = ["Loamy", "Sandy", "Clay", "Silt", "Peaty"]

# Valid Ranges for Validation & Metadata Endpoint
FEATURE_RANGES = {
    "rainfall": {"min": 0.0, "max": 5000.0, "unit": "mm"},
    "temperature": {"min": -10.0, "max": 60.0, "unit": "°C"},
    "humidity": {"min": 0.0, "max": 100.0, "unit": "%"},
    "fertilizer": {"min": 0.0, "max": 2000.0, "unit": "kg/ha"},
    "area": {"min": 0.1, "max": 10000.0, "unit": "ha"},
}

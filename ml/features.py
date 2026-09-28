"""Feature definitions and constants for the ML pipeline."""

# Feature column names
CROP_COL = "crop"
AREA_COL = "area"
RAINFALL_COL = "rainfall"
TEMPERATURE_COL = "temperature"
HUMIDITY_COL = "humidity"
SOIL_TYPE_COL = "soil_type"
FERTILIZER_COL = "fertilizer"
TARGET_COL = "yield"

# All feature columns in order
FEATURE_COLUMNS = [
    CROP_COL,
    AREA_COL,
    RAINFALL_COL,
    TEMPERATURE_COL,
    HUMIDITY_COL,
    SOIL_TYPE_COL,
    FERTILIZER_COL,
]

# Categorical features
CATEGORICAL_FEATURES = [CROP_COL, SOIL_TYPE_COL]

# Numerical features
NUMERICAL_FEATURES = [
    AREA_COL,
    RAINFALL_COL,
    TEMPERATURE_COL,
    HUMIDITY_COL,
    FERTILIZER_COL,
]

# Target
TARGET_COLUMN = TARGET_COL

# Default values for optional features
DEFAULT_FERTILIZER = 0.0

# Model parameters
RANDOM_STATE = 42
TEST_SIZE = 0.2

# Random Forest parameters
RF_N_ESTIMATORS = 100
RF_MAX_DEPTH = None
RF_MIN_SAMPLES_SPLIT = 2
RF_MIN_SAMPLES_LEAF = 1
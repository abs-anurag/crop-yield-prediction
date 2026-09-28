import os


API_VERSION = "1.0.0"

BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))

MODEL_PATH = os.getenv(
    "MODEL_PATH",
    "ml/model/crop_yield_model.joblib",
)

PREPROCESSOR_PATH = os.getenv(
    "PREPROCESSOR_PATH",
    "ml/model/preprocessor.joblib",
)

CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]
from fastapi import APIRouter, Depends
from backend.schemas.response import HealthResponse
from backend.config import get_settings


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint - reflects actual model load status."""
    settings = get_settings()
    
    # Check if model files exist
    import os
    model_exists = os.path.exists(settings.MODEL_PATH)
    preprocessor_exists = os.path.exists(settings.PREPROCESSOR_PATH)
    model_loaded = model_exists and preprocessor_exists
    
    return HealthResponse(
        status="ok",
        model_loaded=model_loaded,
        version="1.0.0"
    )
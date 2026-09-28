from fastapi import APIRouter

from backend.config import API_VERSION
from backend.schemas.response import HealthResponse
from backend.services.prediction import is_model_loaded


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        model_loaded=is_model_loaded(),
        version=API_VERSION,
    )
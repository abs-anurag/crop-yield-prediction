from fastapi import APIRouter
from backend.routes import health, metadata, predict


api_router = APIRouter()

api_router.include_router(health.router, prefix="/api", tags=["health"])
api_router.include_router(metadata.router, prefix="/api", tags=["metadata"])
api_router.include_router(predict.router, prefix="/api", tags=["prediction"])
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import CORS_ORIGINS
from backend.routes.health import router as health_router
from backend.routes.metadata import router as metadata_router
from backend.routes.predict import router as predict_router


app = FastAPI(
    title="AI-Based Crop Yield Prediction API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health_router, prefix="/api")
app.include_router(metadata_router, prefix="/api")
app.include_router(predict_router, prefix="/api")

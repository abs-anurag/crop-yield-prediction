"""FastAPI application for Crop Yield Prediction API."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.routes import api_router
from backend.services.prediction import load_model_artifacts


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - load model at startup."""
    # Startup
    print("Starting Crop Yield Prediction API...")
    load_model_artifacts()
    yield
    # Shutdown
    print("Shutting down...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title="Crop Yield Prediction API",
        description="API for predicting crop yields based on agricultural parameters",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    app.include_router(api_router)
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=True
    )
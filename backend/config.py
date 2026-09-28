from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Backend
    BACKEND_HOST: str = Field(default="0.0.0.0", description="Server host")
    BACKEND_PORT: int = Field(default=8000, description="Server port")
    
    # Model paths
    MODEL_PATH: str = Field(default="ml/model/crop_yield_model.joblib", description="Path to model artifact")
    PREPROCESSOR_PATH: str = Field(default="ml/model/preprocessor.joblib", description="Path to preprocessor artifact")
    
    # CORS
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Allowed CORS origins"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
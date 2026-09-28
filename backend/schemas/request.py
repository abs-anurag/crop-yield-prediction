from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class PredictionRequest(BaseModel):
    """Request schema for crop yield prediction."""
    
    crop: str = Field(..., description="Crop type", examples=["Wheat"])
    area: float = Field(..., gt=0, le=10000, description="Area in hectares")
    rainfall: float = Field(..., ge=0, le=5000, description="Annual rainfall in mm")
    temperature: float = Field(..., ge=-10, le=60, description="Average temperature in °C")
    humidity: float = Field(..., ge=0, le=100, description="Average humidity in %")
    soil_type: str = Field(..., description="Soil type", examples=["Loamy"])
    fertilizer: float = Field(0, ge=0, le=2000, description="Fertilizer in kg/ha")

    @field_validator("crop")
    @classmethod
    def validate_crop(cls, v: str) -> str:
        supported = ["Wheat", "Rice", "Maize", "Cotton", "Sugarcane"]
        if v not in supported:
            raise ValueError(f"Crop must be one of: {', '.join(supported)}")
        return v

    @field_validator("soil_type")
    @classmethod
    def validate_soil_type(cls, v: str) -> str:
        supported = ["Loamy", "Sandy", "Clay", "Silt", "Peaty"]
        if v not in supported:
            raise ValueError(f"Soil type must be one of: {', '.join(supported)}")
        return v


class PredictionRequestList(BaseModel):
    """Batch prediction request."""
    predictions: List[PredictionRequest] = Field(..., min_length=1, max_length=100)
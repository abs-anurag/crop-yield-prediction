from typing import Dict, List

from pydantic import BaseModel


class PredictionResponse(BaseModel):
    predicted_yield: float
    unit: str = "tons/hectare"
    crop: str


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str


class FeatureRange(BaseModel):
    min: float
    max: float
    unit: str


class MetadataResponse(BaseModel):
    supported_crops: List[str]
    supported_soil_types: List[str]
    feature_ranges: Dict[str, FeatureRange]


class ErrorResponse(BaseModel):
    error: str
    message: str
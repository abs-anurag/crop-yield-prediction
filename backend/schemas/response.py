from typing import List, Dict, Any
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field("ok", description="Service status")
    model_loaded: bool = Field(..., description="Whether ML model is loaded")
    version: str = Field("1.0.0", description="API version")


class FeatureRange(BaseModel):
    """Feature range for validation."""
    min: float = Field(..., description="Minimum value (inclusive)")
    max: float = Field(..., description="Maximum value (inclusive)")
    unit: str = Field(..., description="Unit of measurement")


class MetadataResponse(BaseModel):
    """Metadata response for frontend form construction."""
    supported_crops: List[str] = Field(..., description="List of supported crop types")
    supported_soil_types: List[str] = Field(..., description="List of supported soil types")
    feature_ranges: Dict[str, FeatureRange] = Field(..., description="Valid ranges for numeric fields")


class PredictionResponse(BaseModel):
    """Prediction response."""
    predicted_yield: float = Field(..., description="Predicted yield value")
    unit: str = Field("tons/hectare", description="Unit of measurement")
    crop: str = Field(..., description="Crop type from request")


class ValidationErrorDetail(BaseModel):
    """Validation error detail."""
    field: str = Field(..., description="Field name")
    message: str = Field(..., description="Error message")


class ValidationErrorResponse(BaseModel):
    """Validation error response (422)."""
    detail: List[ValidationErrorDetail] = Field(..., description="List of validation errors")


class ModelNotReadyResponse(BaseModel):
    """Model not ready response (503)."""
    error: str = Field("MODEL_NOT_READY", description="Error code")
    message: str = Field(..., description="Human-readable message")


class PredictionErrorResponse(BaseModel):
    """Prediction error response (500)."""
    error: str = Field("PREDICTION_FAILED", description="Error code")
    message: str = Field(..., description="Human-readable message")
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    crop: str = Field(..., min_length=1)
    area: float = Field(..., gt=0, le=10000)
    rainfall: float = Field(..., ge=0, le=5000)
    temperature: float = Field(..., ge=-10, le=60)
    humidity: float = Field(..., ge=0, le=100)
    soil_type: str = Field(..., min_length=1)
    fertilizer: float = Field(default=0.0, ge=0, le=2000)
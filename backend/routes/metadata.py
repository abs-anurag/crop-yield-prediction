from fastapi import APIRouter

from backend.schemas.response import FeatureRange, MetadataResponse


router = APIRouter()


@router.get("/metadata", response_model=MetadataResponse)
def metadata() -> MetadataResponse:
    return MetadataResponse(
        supported_crops=[
            "Wheat",
            "Rice",
            "Maize",
            "Cotton",
            "Sugarcane",
        ],
        supported_soil_types=[
            "Loamy",
            "Sandy",
            "Clay",
            "Silt",
            "Peaty",
        ],
        feature_ranges={
            "rainfall": FeatureRange(min=0, max=5000, unit="mm"),
            "temperature": FeatureRange(min=-10, max=60, unit="°C"),
            "humidity": FeatureRange(min=0, max=100, unit="%"),
            "fertilizer": FeatureRange(min=0, max=2000, unit="kg/ha"),
            "area": FeatureRange(min=0.1, max=10000, unit="ha"),
        },
    )
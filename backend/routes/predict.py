from fastapi import APIRouter, HTTPException, status
from backend.schemas.request import PredictionRequest
from backend.schemas.response import (
    PredictionResponse,
    ValidationErrorResponse,
    ModelNotReadyResponse,
    PredictionErrorResponse,
)
from backend.services.prediction import get_prediction, is_model_loaded


router = APIRouter()


@router.post(
    "/predict",
    response_model=PredictionResponse,
    responses={
        422: {"model": ValidationErrorResponse, "description": "Validation error"},
        503: {"model": ModelNotReadyResponse, "description": "Model not loaded"},
        500: {"model": PredictionErrorResponse, "description": "Prediction failed"},
    },
)
async def predict_yield(request: PredictionRequest):
    """
    Predict crop yield based on agricultural parameters.
    
    Returns predicted yield in tons/hectare.
    """
    # Check if model is loaded
    if not is_model_loaded():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=ModelNotReadyResponse(
                message="ML model is not loaded. Please contact the administrator."
            ).model_dump()
        )
    
    try:
        # Convert request to dict for prediction service
        request_data = request.model_dump()
        
        # Get prediction from ML model
        predicted_yield = get_prediction(request_data)
        
        return PredictionResponse(
            predicted_yield=predicted_yield,
            unit="tons/hectare",
            crop=request.crop
        )
    
    except ValueError as e:
        # Validation or preprocessing errors
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=ValidationErrorResponse(
                detail=[{"field": "input", "message": str(e)}]
            ).model_dump()
        )
    
    except Exception as e:
        # Unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=PredictionErrorResponse(
                message="An error occurred during prediction. Please try again."
            ).model_dump()
        )
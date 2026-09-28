from fastapi import APIRouter
from fastapi.responses import JSONResponse

from backend.schemas.request import PredictionRequest
from backend.schemas.response import PredictionResponse
from backend.services.prediction import get_prediction


router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        prediction = get_prediction(request.model_dump())

        return PredictionResponse(
            predicted_yield=prediction,
            unit="tons/hectare",
            crop=request.crop,
        )

    except RuntimeError as exc:
        if str(exc) == "MODEL_NOT_READY":
            return JSONResponse(
                status_code=503,
                content={
                    "error": "MODEL_NOT_READY",
                    "message": (
                        "ML model is not loaded. "
                        "Please contact the administrator."
                    ),
                },
            )
        raise

    except Exception:
        return JSONResponse(
            status_code=500,
            content={
                "error": "PREDICTION_FAILED",
                "message": (
                    "An error occurred during prediction. "
                    "Please try again."
                ),
            },
        )
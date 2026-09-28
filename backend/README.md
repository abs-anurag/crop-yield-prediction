# Backend API

## Quick Start
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/health | Service health + model status |
| GET | /api/metadata | Crops, soil types, feature ranges |
| POST | /api/predict | Yield prediction |

## API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration
Environment variables (from `.env`):
- `BACKEND_HOST` - Server host (default: 0.0.0.0)
- `BACKEND_PORT` - Server port (default: 8000)
- `MODEL_PATH` - Path to model artifact
- `PREPROCESSOR_PATH` - Path to preprocessor artifact

## CORS
Allowed origins:
- http://localhost:3000
- http://localhost:5173

## Model Integration
The backend loads model artifacts at startup:
```python
model = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)
```

If artifacts not found, `model_loaded` = false in `/api/health`.

## Testing
```bash
pytest ../tests/test_api.py -v
```

## Project Structure
```
backend/
├── main.py              # FastAPI app
├── config.py            # Settings
├── routes/
│   ├── health.py        # GET /api/health
│   ├── metadata.py      # GET /api/metadata
│   └── predict.py       # POST /api/predict
├── services/
│   └── prediction.py    # Model loading + prediction
├── schemas/
│   ├── request.py       # PredictionRequest
│   └── response.py      # Response models
└── README.md
```
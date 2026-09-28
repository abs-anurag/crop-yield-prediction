# AI-Based Crop Yield Prediction - Architecture Document

## System Overview
This document describes the technical architecture for the AI-Based Crop Yield Prediction system. The system follows a four-layer architecture with strict separation of concerns.

## Four-Layer Architecture

### Layer 1: Frontend (Presentation Layer)
**Technology**: React 18 + Vite 5 + TypeScript
**Responsibilities**:
- User interface rendering
- Form state management
- Client-side validation
- API communication
- Result visualization
- UI state management (Normal, Loading, Success, Error)

**Components**:
- `PredictionForm` - Input form with all 7 fields
- `ResultDashboard` - Displays prediction + input summary
- `YieldChart` - Bar chart visualization
- `MetadataProvider` - Fetches and caches `/api/metadata`
- `APIClient` - Axios wrapper for backend communication

**State Management**: React Context + useReducer for prediction flow
**Styling**: CSS Modules or Tailwind CSS (team decision)

**Port**: `http://localhost:5173` (Vite default)

---

### Layer 2: Backend (API Layer)
**Technology**: FastAPI 0.104+ + Uvicorn + Pydantic 2
**Responsibilities**:
- HTTP request/response handling
- Input validation (Pydantic models)
- API endpoint routing
- CORS configuration
- Error handling & structured responses
- Model artifact loading & lifecycle
- Delegation to ML layer

**Module Structure**:
```
backend/
├── main.py              # FastAPI app factory, middleware, router inclusion
├── config.py            # Settings management (pydantic-settings)
├── routes/
│   ├── __init__.py
│   ├── health.py        # GET /api/health
│   ├── metadata.py      # GET /api/metadata
│   └── predict.py       # POST /api/predict
├── services/
│   ├── __init__.py
│   └── prediction.py    # Model loading, predict_yield() delegation
├── schemas/
│   ├── __init__.py
│   ├── request.py       # PredictionRequest (Pydantic)
│   └── response.py      # PredictionResponse, HealthResponse, MetadataResponse
└── README.md
```

**Endpoints**:
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/health | Service health + model load status |
| GET | /api/metadata | Supported crops, soil types, feature ranges |
| POST | /api/predict | Yield prediction with validation |

**CORS Origins**: `http://localhost:3000`, `http://localhost:5173`
**Port**: `http://localhost:8000`

---

### Layer 3: ML Engine (Model Layer)
**Technology**: scikit-learn 1.3+ + pandas 2.0+ + numpy 1.24+ + joblib 1.3+
**Responsibilities**:
- Data preprocessing (training & inference)
- Feature engineering
- Model training & evaluation
- Model persistence
- Prediction interface (`predict_yield()`)

**Module Structure**:
```
ml/
├── __init__.py
├── preprocessing.py   # PreprocessingPipeline class
├── features.py        # Feature definitions, constants, column names
├── train.py           # Training script (baseline + primary model)
├── evaluate.py        # Evaluation metrics (RMSE, MAE, R²)
├── predict.py         # predict_yield(input_dict) -> float
├── model/             # Artifacts (NOT in Git)
│   ├── crop_yield_model.joblib
│   └── preprocessor.joblib
└── README.md
```

**Key Classes/Functions**:
- `PreprocessingPipeline` - Handles all preprocessing (fit/transform)
- `train_baseline_model()` - Linear Regression
- `train_primary_model()` - Random Forest Regressor
- `evaluate_model()` - Returns dict with RMSE, MAE, R²
- `predict_yield(input_dict: dict) -> float` - Main inference function

**Artifacts** (saved via joblib):
1. `crop_yield_model.joblib` - Trained model
2. `preprocessor.joblib` - Fitted preprocessing pipeline

**CRITICAL**: Both artifacts MUST be saved together and loaded together. Preprocessing during inference MUST match training exactly.

---

### Layer 4: Data Layer
**Technology**: pandas + CSV/Parquet files
**Responsibilities**:
- Raw dataset storage
- Processed dataset storage
- Train/test split management

**Structure**:
```
data/
├── raw/               # Original downloaded dataset (NOT in Git)
│   └── crop_yield.csv
├── processed/         # Cleaned, split datasets (NOT in Git)
│   ├── train.csv
│   └── test.csv
└── README.md          # Dataset documentation
```

---

## Data Flow Details

### Training Pipeline
```python
# ml/train.py
def main():
    # 1. Load raw data
    df = pd.read_csv("data/raw/crop_yield.csv")
    
    # 2. PreprocessingPipeline handles everything
    pipeline = PreprocessingPipeline()
    X_train, X_test, y_train, y_test = pipeline.prepare_data(df)
    
    # 3. Train baseline
    baseline = train_baseline_model(X_train, y_train)
    baseline_metrics = evaluate_model(baseline, X_test, y_test)
    
    # 4. Train primary
    model = train_primary_model(X_train, y_train)
    metrics = evaluate_model(model, X_test, y_test)
    
    # 5. Save BOTH artifacts
    joblib.dump(model, "ml/model/crop_yield_model.joblib")
    joblib.dump(pipeline, "ml/model/preprocessor.joblib")
    
    # 6. Log metrics
    print(f"Baseline R²: {baseline_metrics['r2']:.4f}")
    print(f"Primary R²: {metrics['r2']:.4f}")
```

### Inference Pipeline
```python
# ml/predict.py
def predict_yield(input_dict: dict) -> float:
    # Load artifacts
    model = joblib.load("ml/model/crop_yield_model.joblib")
    preprocessor = joblib.load("ml/model/preprocessor.joblib")
    
    # Convert input to DataFrame
    df = pd.DataFrame([input_dict])
    
    # Apply SAME preprocessing (no refitting!)
    X = preprocessor.transform(df)
    
    # Predict
    prediction = model.predict(X)[0]
    return float(prediction)
```

```python
# backend/services/prediction.py
def get_prediction(request_data: dict) -> float:
    from ml.predict import predict_yield
    return predict_yield(request_data)
```

---

## API Contract Enforcement

The API contract is defined in `docs/api.md` and enforced by:
1. **Pydantic Models** (backend/schemas/) - Request/response validation
2. **Type Hints** - Shared between frontend (TypeScript) and backend (Python)
3. **Integration Tests** - `tests/test_api.py` validates contract compliance

**Contract Changes Require**:
1. Update `docs/api.md` FIRST
2. Notify all developers
3. Update backend schemas
4. Update frontend API client
5. Re-test full integration

---

## Error Handling Strategy

| Layer | Error Type | Handling |
|-------|------------|----------|
| Frontend | Validation | Show inline field errors |
| Frontend | Network | Show toast/notification |
| Frontend | 422 | Parse detail, show field-specific messages |
| Frontend | 503 | Show "Model not ready, try again" |
| Backend | Validation | Pydantic → 422 with structured detail |
| Backend | Model missing | 503 with `MODEL_NOT_READY` code |
| Backend | Prediction error | 500 with generic message |
| ML | Preprocessing error | Raise, caught by backend |
| ML | Prediction error | Raise, caught by backend |

---

## Security Considerations
- No authentication (academic demo)
- CORS restricted to known frontend origins
- Input validation on both client and server
- No sensitive data in logs
- Environment variables for configuration
- Model artifacts not in version control

---

## Performance Considerations
- Model loaded once at startup (not per request)
- Preprocessor loaded once at startup
- Frontend caches metadata response
- Vite dev server for fast HMR
- Uvicorn with multiple workers for production (optional)

---

## Deployment Architecture (Future)

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   CDN/      │────▶│  Frontend   │────▶│   Backend   │
│   Static    │     │  (React)    │     │  (FastAPI)  │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                                │
                                                ▼
                                         ┌─────────────┐
                                         │  ML Model   │
                                         │  (Artifacts)│
                                         └─────────────┘
```

---

## Dependencies Between Layers

```
Frontend ──(HTTP/JSON)──▶ Backend ──(Python Call)──▶ ML Engine
                              │
                              ▼
                         Data Layer
                              │
                              ▼
                         Model Artifacts
```

**No Reverse Dependencies**: ML never calls Backend; Backend never calls Frontend

---

## Testing Strategy

| Layer | Unit Tests | Integration Tests |
|-------|------------|-------------------|
| ML | `tests/test_ml.py` - preprocessing, predict_yield | `tests/test_preprocessing.py` - train/serve consistency |
| Backend | `tests/test_api.py` - endpoint validation, schemas | Full API test with mock model |
| Frontend | Component tests (Vitest) | E2E with Playwright (optional) |

---

## Configuration Management

| Config | Location | Environment Variable |
|--------|----------|---------------------|
| Backend host/port | `backend/config.py` | `BACKEND_HOST`, `BACKEND_PORT` |
| Model path | `backend/config.py` | `MODEL_PATH` |
| Preprocessor path | `backend/config.py` | `PREPROCESSOR_PATH` |
| Frontend API URL | `.env.local` | `VITE_API_URL` |

---

## Monitoring & Observability (Minimal for Demo)
- `GET /api/health` returns `model_loaded` status
- Structured logging in backend (stdout)
- Frontend console logs for debugging
- No external APM required for demo
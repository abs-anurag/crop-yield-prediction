# AI-Based Crop Yield Prediction - Project Blueprint

## Project Objective
Build an end-to-end working demonstration of an AI-based crop yield prediction system where users input agricultural parameters (crop type, area, rainfall, temperature, humidity, soil type, fertilizer) and receive a machine learning-based yield prediction with visualization.

## Problem Statement
Farmers and agricultural planners need reliable crop yield predictions to make informed decisions about planting, resource allocation, and harvest planning. Traditional methods rely on historical averages and expert intuition. Machine learning can leverage historical agricultural data to provide more accurate, data-driven predictions.

## Proposed Solution
A web-based application with:
1. **Data Layer**: Public crop yield dataset (FAO/UCI/Kaggle) with features including crop type, area, weather data, soil type, and fertilizer usage
2. **ML Layer**: Preprocessing pipeline + trained Random Forest regressor (with Linear Regression baseline) that predicts yield in tons/hectare
3. **Backend Layer**: FastAPI REST API with validation, health checks, metadata endpoints, and model serving
4. **Frontend Layer**: React + Vite dashboard with dynamic form, real-time validation, loading states, and result visualization

## Target Users
- Agricultural students and researchers (academic demo)
- Farmers seeking yield estimates (potential future users)
- Policy makers evaluating agricultural productivity (potential future users)

## Project Features
1. **Prediction Form**: Input all 7 required agricultural parameters with validation
2. **Dynamic Dropdowns**: Crops and soil types loaded from backend metadata API
3. **Real-time Validation**: Client-side and server-side input validation
4. **Prediction Result**: Display predicted yield with unit and input summary
5. **Visualization**: Bar chart comparing predicted yield to baseline/average
6. **Error Handling**: User-friendly error messages for invalid inputs and system errors
7. **Health Monitoring**: API health endpoint showing model load status

## System Architecture

```
┌──────────────────────────────────────────────┐
│                  FRONTEND                    │
│  React + Vite                                │
│  Prediction Form    Dashboard    Charts      │
│  Input Summary      Results      UI States   │
└──────────────────────┬───────────────────────┘
                       │ REST API (JSON)
                       ▼
┌──────────────────────────────────────────────┐
│                  BACKEND (FastAPI)           │
│  Request Validation    Prediction Service    │
│  API Endpoints         Error Handling        │
│  Health Check          Metadata Endpoint     │
└──────────────────────┬───────────────────────┘
                       │ Python Function Call
                       ▼
┌──────────────────────────────────────────────┐
│                  ML ENGINE                   │
│  Preprocessing      Feature Engineering      │
│  Model Training     Model Evaluation         │
│  Saved Model        predict_yield()          │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│                  DATA LAYER                  │
│  Raw Dataset        Processed Dataset        │
│  Train / Test Split                          │
└──────────────────────────────────────────────┘
```

**Layer Ownership Rules**:
- ML layer owns ALL preprocessing (both training and inference)
- Backend owns API communication and delegates to `predict_yield()`
- Frontend owns presentation only — no ML logic
- Never duplicate preprocessing logic between backend and ML code

## Data Flow

### Training Data Flow
```
Raw Dataset
     ↓
Data Cleaning
     ↓
Missing Value Handling
     ↓
Categorical Encoding (LabelEncoder / OneHotEncoder)
     ↓
Numerical Scaling (StandardScaler / MinMaxScaler)
     ↓
Feature Engineering
     ↓
Train / Test Split (80/20)
     ↓
Model Training (Linear Regression → Random Forest)
     ↓
Model Evaluation (RMSE, MAE, R²)
     ↓
Save Model Artifact         → ml/model/crop_yield_model.joblib
Save Preprocessor Artifact  → ml/model/preprocessor.joblib
```

### Prediction Data Flow
```
User Input (Web Form)
     ↓
Frontend Validation
     ↓
POST /api/predict (JSON)
     ↓
FastAPI: Pydantic Validation
     ↓
Backend Prediction Service
     ↓
Load preprocessor.joblib
     ↓
Load crop_yield_model.joblib
     ↓
predict_yield(input_dict)
     ↓
Predicted Yield (float)
     ↓
Backend JSON Response
     ↓
Frontend Dashboard
     ↓
Result + Visualization
```

## ML Pipeline
1. **Data Source**: FAO/UCI public crop yield dataset
2. **Features**: crop (categorical), area (numeric), rainfall (numeric), temperature (numeric), humidity (numeric), soil_type (categorical), fertilizer (numeric)
3. **Target**: yield (tons/hectare)
4. **Preprocessing**: Label encoding for categoricals, standard scaling for numerics
5. **Models**: 
   - Baseline: Linear Regression
   - Primary: Random Forest Regressor (n_estimators=100, random_state=42)
   - Optional: XGBoost (if time permits)
6. **Evaluation**: RMSE, MAE, R² on test set
7. **Artifacts**: model.joblib + preprocessor.joblib (MUST be used together)

## Frontend Flow
1. App loads → `GET /api/metadata` → populate crop & soil type dropdowns
2. User fills form → client-side validation (required fields, numeric ranges)
3. Submit → `POST /api/predict` → show Loading state
4. Success → display yield, unit, input summary, bar chart
5. Error → show user-friendly message (not raw error)
6. Reset → clear form, return to Normal state

## Backend Flow
1. Startup → load model + preprocessor artifacts → set `model_loaded` flag
2. `GET /api/health` → return status + `model_loaded` boolean
3. `GET /api/metadata` → return supported crops, soil types, feature ranges from dataset
4. `POST /api/predict` → Pydantic validation → call `predict_yield()` → return prediction
5. Validation errors → 422 with structured detail
6. Model not loaded → 503 with error code

## API Contract (FROZEN - See docs/api.md)

### GET /api/health
```json
{"status": "ok", "model_loaded": true, "version": "1.0.0"}
```

### GET /api/metadata
```json
{
  "supported_crops": ["Wheat", "Rice", "Maize", "Cotton", "Sugarcane"],
  "supported_soil_types": ["Loamy", "Sandy", "Clay", "Silt", "Peaty"],
  "feature_ranges": {
    "rainfall": {"min": 0, "max": 5000, "unit": "mm"},
    "temperature": {"min": -10, "max": 60, "unit": "°C"},
    "humidity": {"min": 0, "max": 100, "unit": "%"},
    "fertilizer": {"min": 0, "max": 2000, "unit": "kg/ha"},
    "area": {"min": 0.1, "max": 10000, "unit": "ha"}
  }
}
```

### POST /api/predict
Request:
```json
{
  "crop": "Wheat",
  "area": 10.0,
  "rainfall": 600.0,
  "temperature": 25.0,
  "humidity": 65.0,
  "soil_type": "Loamy",
  "fertilizer": 100.0
}
```
Response (200):
```json
{"predicted_yield": 42.5, "unit": "tons/hectare", "crop": "Wheat"}
```

## Technology Stack
| Layer | Technology | Version |
|-------|------------|---------|
| Language | Python | 3.10 or 3.11 |
| ML | scikit-learn, pandas, numpy, joblib | See requirements.txt |
| ML Optional | XGBoost | Only if time allows |
| Backend | FastAPI + Uvicorn + Pydantic | See requirements.txt |
| Frontend | React + Vite | Latest |
| Testing | pytest + httpx | See requirements.txt |
| EDA | Jupyter + matplotlib + seaborn | See requirements.txt |

## Team Responsibilities

### Developer 1 - Data & ML (Branch: `feature/data-ml`)
- Owns: `data/`, `ml/`, `notebooks/`
- Dataset acquisition, EDA, preprocessing, training, evaluation, prediction interface
- Delivers: `ml/predict.py`, `ml/model/*.joblib`

### Developer 2 - Backend (Branch: `feature/backend`)
- Owns: `backend/`
- FastAPI app, API endpoints, Pydantic schemas, prediction service, model integration
- Delivers: Working API at `http://localhost:8000`

### Developer 3 - Frontend (Branch: `feature/frontend`)
- Owns: `frontend/`
- React + Vite app, form, validation, UI states, dashboard, visualization, API integration
- Delivers: Working UI at `http://localhost:5173`

## GitHub Branch Strategy
- `main` — Stable, integrated project only
- `feature/data-ml` — Developer 1 work
- `feature/backend` — Developer 2 work
- `feature/frontend` — Developer 3 work

## 2-Day Development Plan

### DAY 1 — BUILD
**Morning (Together)**:
- Agree on dataset, features, API contract, frontend framework
- Create repository, branches, documentation scaffold

**Morning (Individual)**:
- Dev 1: Download dataset, begin EDA
- Dev 2: Scaffold FastAPI, CORS, GET /api/health
- Dev 3: Scaffold React+Vite, env var setup, fetch metadata

**Afternoon (Individual)**:
- Dev 1: Preprocessing pipeline, baseline model, begin Random Forest
- Dev 2: GET /api/metadata, POST /api/predict (mock), Pydantic schemas
- Dev 3: Build prediction form, validation, UI states, connect mock JSON

**Evening (Individual)**:
- Dev 1: Train/evaluate final model, save artifacts, communicate checkpoint
- Dev 2: Write API tests, integrate model if available
- Dev 3: Build result dashboard, visualization, confirm frontend running

### DAY 2 — INTEGRATE, FIX, POLISH
**Morning**: Execute Checkpoints 1, 2, 3 (Full E2E integration)
**Midday**: Fix integration bugs, API mismatches, preprocessing issues
**Afternoon**: Polish UI, improve errors, add visualization, run tests
**Evening**: Remove mocks, update docs, clean repo, final E2E demo, PRs, merge

## Future Enhancements (Post-MVP)
- Multiple model comparison UI
- Historical prediction tracking
- Geographic visualization (maps)
- Weather API integration for auto-population
- Multi-language support
- Export predictions to PDF/CSV
- User authentication and saved predictions
- Model retraining pipeline
- Mobile-responsive design improvements

## Project Constraints
- **Database**: None — use model + preprocessor artifacts only
- **Authentication**: None
- **Deployment**: Local demo first; cloud optional after local works
- **Model Artifacts**: Not committed to Git — share via file transfer
- **Scope**: No auth, databases, microservices, cloud, multiple models, disease detection, irrigation, market prices, weather APIs, IoT sensors

**MVP = Agricultural Input → ML → Crop Yield Prediction → Web Dashboard**
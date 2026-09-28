# AI-Based Crop Yield Prediction

> An end-to-end machine learning demonstration for predicting crop yields based on agricultural parameters.

## Overview

This project demonstrates a complete ML pipeline from data to deployment: a web application where users input agricultural parameters (crop type, area, weather conditions, soil type, fertilizer usage) and receive an AI-powered yield prediction in tons per hectare.

## Problem Statement

Agricultural yield prediction is critical for food security, farmer income stability, and resource planning. Traditional methods rely on historical averages and expert judgment. This project showcases how machine learning can leverage historical agricultural data to provide more accurate, data-driven predictions.

## Proposed Solution

A four-layer architecture:
1. **Data Layer** - Public crop yield dataset (FAO/UCI)
2. **ML Layer** - Preprocessing pipeline + Random Forest regressor
3. **Backend Layer** - FastAPI REST API with validation and model serving
4. **Frontend Layer** - React + Vite dashboard with real-time validation and visualization

## Features

- 🌾 **Multi-crop Support**: Wheat, Rice, Maize, Cotton, Sugarcane
- 🌱 **Soil Type Awareness**: Loamy, Sandy, Clay, Silt, Peaty
- 🌤️ **Weather Parameters**: Rainfall, temperature, humidity
- 💊 **Fertilizer Input**: Optional fertilizer application rate
- ✅ **Real-time Validation**: Client-side and server-side
- 📊 **Visualization**: Predicted yield with comparison chart
- 🔄 **Loading States**: Smooth UX during prediction
- ⚠️ **Error Handling**: User-friendly error messages
- 🏥 **Health Monitoring**: API status and model readiness

## System Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│   Backend   │────▶│    ML       │────▶│    Data     │
│  (React)    │     │  (FastAPI)  │     │  Engine     │     │  Layer      │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
    Port 5173         Port 8000         Python Functions      CSV Files
```

## Data Flow

**Training**: Raw Data → Cleaning → Encoding → Scaling → Feature Engineering → Train/Test Split → Model Training → Evaluation → Save Artifacts

**Prediction**: User Input → Frontend Validation → POST /api/predict → Backend Validation → Load Artifacts → Preprocess → Predict → JSON Response → Frontend Display

## Technology Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10/3.11 |
| ML | scikit-learn, pandas, numpy, joblib |
| Backend | FastAPI, Uvicorn, Pydantic |
| Frontend | React 18, Vite 5 |
| Testing | pytest, httpx |
| EDA | Jupyter, matplotlib, seaborn |

## Repository Structure

```
crop-yield-prediction/
├── data/
│   ├── raw/              # Original dataset (not in Git)
│   ├── processed/        # Cleaned/split data (not in Git)
│   └── README.md         # Dataset documentation
├── ml/
│   ├── preprocessing.py  # Preprocessing pipeline
│   ├── features.py       # Feature definitions
│   ├── train.py          # Training script
│   ├── evaluate.py       # Evaluation metrics
│   ├── predict.py        # predict_yield() interface
│   ├── model/            # Artifacts (not in Git)
│   └── README.md
├── backend/
│   ├── main.py           # FastAPI app
│   ├── config.py         # Settings
│   ├── routes/           # API endpoints
│   ├── services/         # Business logic
│   ├── schemas/          # Pydantic models
│   └── README.md
├── frontend/
│   └── src/              # React + Vite app
├── tests/
│   ├── test_ml.py
│   ├── test_api.py
│   └── test_preprocessing.py
├── notebooks/
│   └── exploration.ipynb
├── docs/
│   ├── blueprint.md
│   ├── architecture.md
│   └── api.md
├── README.md
├── DEVELOPMENT.md
├── AGENTS.md
├── requirements.txt
├── .gitignore
└── .env.example
```

## Installation

### Prerequisites
- Python 3.10 or 3.11
- Node.js 18+ (for frontend)
- Git

### Backend Setup
```bash
# Clone repository
git clone https://github.com/<username>/crop-yield-prediction.git
cd crop-yield-prediction

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env if needed
```

### Frontend Setup
```bash
cd frontend
npm install
# Create .env.local with VITE_API_URL=http://localhost:8000
```

## Running the Project

### 1. Train the Model (Developer 1)
```bash
# From project root
cd ml
python train.py
# Outputs: ml/model/crop_yield_model.joblib, ml/model/preprocessor.joblib
```

### 2. Start Backend (Developer 2)
```bash
# From project root
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### 3. Start Frontend (Developer 3)
```bash
# From project root
cd frontend
npm run dev
# App available at http://localhost:5173
```

### 4. Full Demo
1. Open http://localhost:5173
2. Fill in the prediction form
3. Click "Predict Yield"
4. View result with visualization

## API Usage

### Health Check
```bash
curl http://localhost:8000/api/health
```

### Get Metadata (for form options)
```bash
curl http://localhost:8000/api/metadata
```

### Make Prediction
```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "crop": "Wheat",
    "area": 10.0,
    "rainfall": 600.0,
    "temperature": 25.0,
    "humidity": 65.0,
    "soil_type": "Loamy",
    "fertilizer": 100.0
  }'
```

### Example Response
```json
{
  "predicted_yield": 4.25,
  "unit": "tons/hectare",
  "crop": "Wheat"
}
```

## Dataset

**Source**: [FAO / UCI / Kaggle - to be determined]
**License**: [To be documented]
**Features**: crop, area, rainfall, temperature, humidity, soil_type, fertilizer
**Target**: yield (tons/hectare)
**Records**: [To be documented]
**Geographic Scope**: [To be documented]

*Full documentation in `data/README.md`*

## Model Evaluation

| Model | RMSE | MAE | R² |
|-------|------|-----|-----|
| Linear Regression (Baseline) | TBD | TBD | TBD |
| Random Forest (Primary) | TBD | TBD | TBD |

*Real metrics only - documented in `ml/README.md` after training*

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for:
- Detailed setup instructions
- Model training steps
- How to share model artifacts between developers
- Common troubleshooting

See [AGENTS.md](AGENTS.md) for:
- Team responsibilities
- Branch ownership
- Integration checkpoints
- Daily sync checklist

## Team

- **Developer 1** (Data & ML): `feature/data-ml` branch
- **Developer 2** (Backend): `feature/backend` branch
- **Developer 3** (Frontend): `feature/frontend` branch

## Future Scope

- Multiple model comparison UI
- Historical prediction tracking
- Geographic visualization
- Weather API integration
- User authentication
- Model retraining pipeline
- Mobile-responsive improvements

## License

Academic / Demonstration Project
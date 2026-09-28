# Development Guide

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.10 or 3.11 | Backend & ML |
| Node.js | 18+ | Frontend |
| Git | Latest | Version control |
| GitHub CLI (gh) | 2.100+ | Repository management |

Verify installations:
```bash
python --version
node --version
git --version
gh --version
```

## Virtual Environment Setup

```bash
# From project root
python -m venv venv

# Activate
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

## Dependency Installation

```bash
# Backend + ML dependencies
pip install -r requirements.txt

# Frontend dependencies
cd frontend
npm install
cd ..
```

## Dataset Setup

### 1. Download Dataset
```bash
# Developer 1: Download from Kaggle/FAO/UCI
# Place in data/raw/
cp /path/to/downloaded/dataset.csv data/raw/crop_yield.csv
```

### 2. Document Dataset
Edit `data/README.md` with:
- Dataset name and source URL
- License
- Feature list and descriptions
- Target variable
- Number of records
- Geographic scope
- Date range
- Known limitations

### 3. Explore Data
```bash
# Start Jupyter for EDA
jupyter notebook notebooks/exploration.ipynb
```

## ML Model Training

### 1. Run Training Script
```bash
cd ml
python train.py
```

### 2. Expected Output
```
Training baseline (Linear Regression)...
Baseline RMSE: X.XX, MAE: X.XX, R²: X.XX

Training primary (Random Forest)...
Primary RMSE: X.XX, MAE: X.XX, R²: X.XX

Saving model to ml/model/crop_yield_model.joblib
Saving preprocessor to ml/model/preprocessor.joblib
```

### 3. Verify Artifacts
```bash
ls -la ml/model/
# Should show:
# crop_yield_model.joblib
# preprocessor.joblib
```

### 4. Document Metrics
Edit `ml/README.md` with actual metrics:
```markdown
## Model Performance (Test Set)

| Model | RMSE | MAE | R² |
|-------|------|-----|-----|
| Linear Regression | X.XX | X.XX | X.XX |
| Random Forest | X.XX | X.XX | X.XX |

**Dataset**: [name], [N] records, [date range]
**Features**: [list]
**Target**: yield (tons/hectare)
```

## Backend Startup

```bash
# From project root
cd backend

# Development mode (auto-reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Verify Backend
```bash
# Health check
curl http://localhost:8000/api/health
# Expected: {"status":"ok","model_loaded":true,"version":"1.0.0"}

# Metadata
curl http://localhost:8000/api/metadata
# Expected: crops, soil_types, feature_ranges

# API Docs
open http://localhost:8000/docs
```

## Frontend Startup

```bash
cd frontend

# Development mode
npm run dev
# Opens http://localhost:5173

# Build for production
npm run build
npm run preview
```

### Environment Configuration
Create `frontend/.env.local`:
```env
VITE_API_URL=http://localhost:8000
```

## Running Tests

### All Tests
```bash
# From project root
pytest tests/ -v
```

### Specific Test Files
```bash
# ML tests
pytest tests/test_ml.py -v

# API tests
pytest tests/test_api.py -v

# Preprocessing tests
pytest tests/test_preprocessing.py -v
```

### Test Coverage
```bash
pytest tests/ --cov=ml --cov=backend --cov-report=term-missing
```

## Sharing Model Artifacts

**IMPORTANT**: Model artifacts (`*.joblib`) are in `.gitignore` and NOT committed to Git.

### Method 1: Direct File Copy (Recommended for 2-day project)
```bash
# Developer 1 shares with Developer 2
# Copy ml/model/ contents to Developer 2's local ml/model/
scp ml/model/*.joblib user@dev2-machine:/path/to/project/ml/model/
# OR use shared drive, USB, email, etc.
```

### Method 2: Cloud Storage (If Available)
```bash
# Upload to Google Drive / OneDrive / Dropbox
# Share link with team
```

### Method 3: Git LFS (For Larger Teams)
```bash
# Not recommended for this short project
git lfs track "ml/model/*.joblib"
git add .gitattributes ml/model/*.joblib
git commit -m "Add model artifacts via LFS"
```

**Document the chosen method here**: [Team to fill in]

## Common Troubleshooting

### Backend: Model Not Loaded
```bash
# Check artifacts exist
ls -la ml/model/

# Check paths in .env
cat .env

# Check backend logs for error messages
```

### Backend: CORS Errors
```bash
# Verify CORS origins in backend/main.py
# Should include: http://localhost:3000, http://localhost:5173
```

### Frontend: API Connection Failed
```bash
# Check VITE_API_URL in frontend/.env.local
cat frontend/.env.local

# Verify backend is running
curl http://localhost:8000/api/health
```

### Frontend: Metadata Not Loading
```bash
# Check browser console for errors
# Verify /api/metadata returns 200
curl http://localhost:8000/api/metadata
```

### ML: Preprocessing Mismatch
```bash
# Ensure SAME preprocessor used for train and predict
# Check ml/predict.py loads preprocessor.joblib
# Check backend/services/prediction.py uses ml.predict.predict_yield
```

### ML: Import Errors
```bash
# Ensure project root is in PYTHONPATH
export PYTHONPATH=/path/to/project:$PYTHONPATH
# Or run from project root
python -m ml.train
```

### Git: Branch Issues
```bash
# Check current branch
git branch

# Switch branch
git checkout feature/data-ml

# Pull latest
git pull origin feature/data-ml

# Check status
git status
```

### Git: Merge Conflicts
```bash
# On feature branch
git fetch origin
git rebase origin/main
# Resolve conflicts
git add .
git rebase --continue
git push --force-with-lease origin feature/<branch>
```

## Environment Variables Reference

### Backend (.env)
```env
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
MODEL_PATH=ml/model/crop_yield_model.joblib
PREPROCESSOR_PATH=ml/model/preprocessor.joblib
```

### Frontend (frontend/.env.local)
```env
VITE_API_URL=http://localhost:8000
```

## Useful Commands

```bash
# View project structure
tree -I 'node_modules|venv|__pycache__|.git'

# Check disk usage
du -sh data/ ml/model/ frontend/node_modules/

# Kill process on port 8000
# Windows: netstat -ano | findstr :8000 → taskkill /PID <pid> /F
# Linux/macOS: lsof -ti:8000 | xargs kill -9

# Kill process on port 5173
# Windows: netstat -ano | findstr :5173 → taskkill /PID <pid> /F
# Linux/macOS: lsof -ti:5173 | xargs kill -9
```

## Code Quality

### Linting (Optional)
```bash
# Python
pip install ruff
ruff check ml/ backend/

# Type checking
pip install mypy
mypy ml/ backend/

# Frontend
cd frontend
npm run lint
```

### Formatting
```bash
# Python
pip install black
black ml/ backend/

# Frontend
cd frontend
npm run format
```

## Git Workflow Reminders

```bash
# Before starting work
git checkout feature/<your-branch>
git pull origin feature/<your-branch>

# After changes
git add .
git commit -m "type(scope): short description"
# Types: feat, fix, docs, test, refactor, chore
# Scopes: ml, api, ui, data, deps, config

# Push
git push origin feature/<your-branch>
```

### Good Commit Messages
```
feat(data): download and document crop yield dataset
feat(ml): implement preprocessing pipeline with label encoding
feat(ml): train random forest regressor, R2=0.87 on test set
feat(api): implement GET /api/health and GET /api/metadata
feat(api): implement POST /api/predict with mock response
feat(api): integrate trained ML model into prediction service
feat(ui): scaffold React app with Vite
feat(ui): build prediction form with validation
feat(ui): implement loading, success, and error states
feat(ui): add yield prediction result dashboard
fix(api): handle unsupported crop with 422 response
fix(ml): fix preprocessor not saved alongside model
test(api): add pytest tests for prediction endpoint
docs(api): freeze API contract in docs/api.md
```

### Bad Commit Messages (Avoid)
```
update
changes
fixed
done
final
FINAL FINAL
it works now
asdf
```
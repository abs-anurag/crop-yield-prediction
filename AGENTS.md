# Team Coordination - AGENTS.md

## Developer Responsibilities

### Developer 1: Data & Machine Learning
**Branch**: `feature/data-ml`
**Owns**: `data/`, `ml/`, `notebooks/`

**Responsibilities**:
- [ ] Find and download public crop yield dataset (FAO/UCI/Kaggle)
- [ ] Document dataset in `data/README.md` (source, license, features, target, records, scope, limitations)
- [ ] Perform EDA in `notebooks/exploration.ipynb`
- [ ] Implement preprocessing pipeline (`ml/preprocessing.py`)
- [ ] Define features and constants (`ml/features.py`)
- [ ] Train baseline model (Linear Regression) in `ml/train.py`
- [ ] Train primary model (Random Forest) in `ml/train.py`
- [ ] Evaluate models (RMSE, MAE, R²) in `ml/evaluate.py`
- [ ] Implement prediction interface `predict_yield(input_dict) -> float` in `ml/predict.py`
- [ ] Save BOTH artifacts: `crop_yield_model.joblib` + `preprocessor.joblib`
- [ ] Document REAL metrics in `ml/README.md` (never fabricate)
- [ ] Communicate Checkpoint 1 readiness to Developer 2

**Current Status**: `COMPLETED`
**Blocked By**: Nothing

---

### Developer 2: Backend API
**Branch**: `feature/backend`
**Owns**: `backend/`

**Responsibilities**:
- [ ] Scaffold FastAPI app in `backend/main.py`
- [ ] Configure CORS for `http://localhost:3000`, `http://localhost:5173`
- [ ] Implement `GET /api/health` - reflect actual model load status
- [ ] Implement `GET /api/metadata` - serve dynamic crop/soil lists from dataset
- [ ] Implement `POST /api/predict` with Pydantic validation
- [ ] Create request schema in `backend/schemas/request.py`
- [ ] Create response schema in `backend/schemas/response.py`
- [ ] Implement prediction service in `backend/services/prediction.py`
- [ ] Replace mock with real model integration after Checkpoint 1
- [ ] Write API tests in `tests/test_api.py`
- [ ] Keep `docs/api.md` synchronized with implementation
- [ ] Communicate Checkpoint 2 readiness to Developer 3

**Current Status**: `NOT_STARTED`
**Blocked By**: Nothing (uses mock prediction on Day 1)

---

### Developer 3: Frontend UI
**Branch**: `feature/frontend`
**Owns**: `frontend/`

**Responsibilities**:
- [ ] Scaffold React + Vite application
- [ ] Configure `VITE_API_URL` environment variable
- [ ] On app load: fetch `GET /api/metadata` and populate dropdowns dynamically
- [ ] Build prediction form with all 7 fields
- [ ] Add client-side validation (required, numeric ranges from metadata)
- [ ] Implement 4 UI states: Normal, Loading, Success, Error
- [ ] Display predicted yield, unit, and input summary
- [ ] Add visualization (bar chart comparing to average/baseline)
- [ ] Handle API errors gracefully (user-friendly messages)
- [ ] Use mock JSON file on Day 1: `frontend/src/mock/prediction-response.json`
- [ ] Replace mock with real API calls at Checkpoint 2

**Current Status**: `NOT_STARTED`
**Blocked By**: Nothing (uses mock JSON on Day 1)

---

## Branch Ownership

| Branch | Owner | Purpose |
|--------|-------|---------|
| `main` | All (merged via PR) | Stable, integrated project |
| `feature/data-ml` | Developer 1 | Dataset, ML training, artifacts |
| `feature/backend` | Developer 2 | FastAPI, endpoints, model serving |
| `feature/frontend` | Developer 3 | React app, UI, visualization |

**Rules**:
- Never commit directly to `main`
- Work only on assigned branch
- Create Pull Request to merge into `main`
- Do not force-push shared branches
- Keep branches up to date with `main`

---

## API Contract Reference

**Location**: `docs/api.md` (FROZEN)

### Endpoints
| Method | Path | Owner | Status |
|--------|------|-------|--------|
| GET | `/api/health` | Dev 2 | FROZEN |
| GET | `/api/metadata` | Dev 2 | FROZEN |
| POST | `/api/predict` | Dev 2 | FROZEN |

### Request/Response Models
Defined in `backend/schemas/` - shared understanding between Dev 2 and Dev 3.

### Change Process
1. Update `docs/api.md` FIRST
2. Notify all developers
3. Update backend schemas
4. Update frontend API client
5. Re-run integration tests

---

## Integration Checkpoints

### Checkpoint 1: ML → Backend
**Trigger**: Developer 1 delivers:
- [ ] `ml/predict.py` complete with `predict_yield()`
- [ ] `ml/model/crop_yield_model.joblib` exists
- [ ] `ml/model/preprocessor.joblib` exists

**Developer 2 Actions**:
- [ ] Pull `feature/data-ml` branch
- [ ] Copy model artifacts to local `ml/model/`
- [ ] Replace mock in `backend/services/prediction.py`
- [ ] Test `POST /api/predict` with real model
- [ ] Verify `GET /api/health` returns `model_loaded: true`
- [ ] Signal completion to team

**Status**: `READY`

---

### Checkpoint 2: Backend → Frontend
**Trigger**: Developer 2 confirms:
- [ ] Backend running at `http://localhost:8000`
- [ ] `GET /api/health` returns `model_loaded: true`
- [ ] `POST /api/predict` returns real predictions

**Developer 3 Actions**:
- [ ] Replace mock JSON with real API calls
- [ ] Set `VITE_API_URL=http://localhost:8000` in `.env.local`
- [ ] Test full frontend → backend prediction flow
- [ ] Verify all UI states work with real API
- [ ] Signal completion to team

**Status**: `PENDING`

---

### Checkpoint 3: Full End-to-End Test
**All Developers Participate**

**Test Flow**:
```
Frontend form submit
       ↓
POST /api/predict
       ↓
Backend validation (Pydantic)
       ↓
prediction_service.get_prediction()
       ↓
ml.predict.predict_yield()
       ↓
Real ML model (Random Forest)
       ↓
JSON response
       ↓
Frontend result display + visualization
```

**Verification**:
- [ ] Valid input → prediction displayed with chart
- [ ] Invalid input → user-friendly field errors
- [ ] Missing model → 503 handled gracefully
- [ ] Network error → toast notification
- [ ] Loading state visible during request
- [ ] Input summary matches submitted data

**Status**: `PENDING`

---

## How to Signal a Blocker

**In GitHub Issues** (or team chat):
```
[BLOCKER] <Developer Name> - <Branch>
Issue: <one-line description>
Details: <what's happening, what was tried>
Need: <specific help needed from whom>
```

**Examples**:
```
[BLOCKER] Dev 1 - feature/data-ml
Issue: Dataset not found with required features
Details: Searched Kaggle/FAO/UCI, no dataset has all 7 features
Need: Dev 2/3 to confirm which features are mandatory vs optional

[BLOCKER] Dev 2 - feature/backend
Issue: Model artifacts not loading
Details: FileNotFoundError for preprocessor.joblib
Need: Dev 1 to share artifacts via [method]
```

**Response Time**: Team should respond within 30 minutes during work hours.

---

## Daily Sync Checklist

### Morning Sync (15 minutes)
- [ ] Each dev: What did you complete yesterday?
- [ ] Each dev: What will you tackle today?
- [ ] Each dev: Any blockers?
- [ ] Team: Any API contract changes needed?
- [ ] Team: Checkpoint status review

### Evening Sync (10 minutes)
- [ ] Each dev: Push current work to branch
- [ ] Each dev: Update status in this file
- [ ] Team: Confirm next day's priorities
- [ ] Team: Verify no broken main branch

---

## Communication Channels

| Purpose | Channel |
|---------|---------|
| Blockers | GitHub Issues + @mention |
| Quick questions | Team chat (Slack/Discord/Teams) |
| Code review | GitHub Pull Requests |
| Documentation updates | Direct commits to docs/ |
| Architecture decisions | This file + team discussion |

---

## Definition of Done

### Per Feature
- [ ] Code complete and tested locally
- [ ] Unit tests pass
- [ ] No linting errors
- [ ] Documentation updated
- [ ] Pushed to feature branch
- [ ] Pull Request created

### Per Integration Checkpoint
- [ ] Both developers verify working integration
- [ ] No mock code in production path
- [ ] Error cases handled
- [ ] API contract compliance verified

### Final Demo
- [ ] All checklist items in blueprint.md pass
- [ ] Clean repository (no secrets, no .env, no artifacts in Git)
- [ ] All branches merged to main
- [ ] README and docs current

---

## Emergency Contacts

| Role | Name | Contact |
|------|------|---------|
| Lead Architect | [Name] | [Contact] |
| Dev 1 (ML) | [Name] | [Contact] |
| Dev 2 (Backend) | [Name] | [Contact] |
| Dev 3 (Frontend) | [Name] | [Contact] |

---

## Notes

- This file is the single source of truth for team coordination
- Update status fields as work progresses
- Add blockers immediately when they occur
- Check this file at each daily sync
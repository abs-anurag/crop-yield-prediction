# AI-Based Crop Yield Prediction - API Contract

**Version**: 1.0.0
**Status**: FROZEN - Do not modify without team coordination
**Last Updated**: 2026-09-28

---

## Base URL
```
http://localhost:8000/api
```

## Content Type
All requests and responses use `application/json`.

---

## Endpoints

### 1. Health Check
**GET** `/health`

#### Description
Returns the service health status and model load status. Frontend should call this on load to verify backend availability.

#### Response (200 OK)
```json
{
  "status": "ok",
  "model_loaded": true,
  "version": "1.0.0"
}
```

#### Fields
| Field | Type | Description |
|-------|------|-------------|
| status | string | Always "ok" if service is running |
| model_loaded | boolean | **Must reflect actual model state** - true if both model and preprocessor artifacts loaded successfully |
| version | string | API version (semver) |

#### Notes
- `model_loaded` MUST NOT be hardcoded to `true`
- Returns 503 if service is starting up but model not yet loaded

---

### 2. Metadata
**GET** `/metadata`

#### Description
Returns dynamic metadata for frontend form construction. Frontend MUST call this on load - do NOT hardcode crop lists, soil types, or ranges in frontend.

#### Response (200 OK)
```json
{
  "supported_crops": ["Wheat", "Rice", "Maize", "Cotton", "Sugarcane"],
  "supported_soil_types": ["Loamy", "Sandy", "Clay", "Silt", "Peaty"],
  "feature_ranges": {
    "rainfall": { "min": 0, "max": 5000, "unit": "mm" },
    "temperature": { "min": -10, "max": 60, "unit": "°C" },
    "humidity": { "min": 0, "max": 100, "unit": "%" },
    "fertilizer": { "min": 0, "max": 2000, "unit": "kg/ha" },
    "area": { "min": 0.1, "max": 10000, "unit": "ha" }
  }
}
```

#### Fields
| Field | Type | Description |
|-------|------|-------------|
| supported_crops | string[] | Crop names from dataset (unique values in crop column) |
| supported_soil_types | string[] | Soil types from dataset (unique values in soil_type column) |
| feature_ranges | object | Valid input ranges for numeric fields |

#### Feature Ranges Structure
Each numeric field has:
- `min`: number (inclusive minimum)
- `max`: number (inclusive maximum)
- `unit`: string (display unit)

#### Notes
- Crop and soil type lists MUST come from actual dataset
- Feature ranges SHOULD reflect realistic agricultural bounds
- Frontend uses these for dropdown options and client-side validation

---

### 3. Prediction
**POST** `/predict`

#### Description
Submits agricultural parameters for yield prediction. Returns predicted yield in tons/hectare.

#### Request Body
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

#### Request Fields
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| crop | string | Yes | Must be in `supported_crops` from `/metadata` |
| area | number | Yes | > 0 and ≤ 10,000 (hectares) |
| rainfall | number | Yes | ≥ 0 and ≤ 5,000 (mm/year) |
| temperature | number | Yes | ≥ -10 and ≤ 60 (°C) |
| humidity | number | Yes | ≥ 0 and ≤ 100 (%) |
| soil_type | string | Yes | Must be in `supported_soil_types` from `/metadata` |
| fertilizer | number | No | ≥ 0 and ≤ 2,000 (kg/ha). Default: 0 |

#### Success Response (200 OK)
```json
{
  "predicted_yield": 42.5,
  "unit": "tons/hectare",
  "crop": "Wheat"
}
```

#### Response Fields
| Field | Type | Description |
|-------|------|-------------|
| predicted_yield | number | Model prediction (float) |
| unit | string | Always "tons/hectare" |
| crop | string | Echo of input crop for confirmation |

---

## Error Responses

### Validation Error (422 Unprocessable Entity)
Returned when request body fails Pydantic validation.

```json
{
  "detail": [
    {
      "field": "rainfall",
      "message": "value must be greater than or equal to 0"
    },
    {
      "field": "crop",
      "message": "value must be one of: Wheat, Rice, Maize, Cotton, Sugarcane"
    }
  ]
}
```

#### Error Detail Structure
| Field | Type | Description |
|-------|------|-------------|
| field | string | Name of the invalid field |
| message | string | Human-readable validation error |

---

### Model Not Ready (503 Service Unavailable)
Returned when model artifacts are not loaded.

```json
{
  "error": "MODEL_NOT_READY",
  "message": "ML model is not loaded. Please contact the administrator."
}
```

#### Error Fields
| Field | Type | Description |
|-------|------|-------------|
| error | string | Error code: "MODEL_NOT_READY" |
| message | string | Human-readable message |

---

### Internal Server Error (500)
Returned for unexpected prediction failures.

```json
{
  "error": "PREDICTION_FAILED",
  "message": "An error occurred during prediction. Please try again."
}
```

---

## HTTP Status Codes Summary

| Code | Scenario |
|------|----------|
| 200 | Successful prediction |
| 422 | Request validation failed |
| 500 | Unexpected server error |
| 503 | Model not loaded |

---

## Example Usage

### cURL Health Check
```bash
curl http://localhost:8000/api/health
```

### cURL Metadata
```bash
curl http://localhost:8000/api/metadata
```

### cURL Prediction
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

### JavaScript (Frontend)
```javascript
// Fetch metadata on app load
const metadata = await fetch(`${API_URL}/metadata`).then(r => r.json());

// Submit prediction
const response = await fetch(`${API_URL}/predict`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    crop: 'Wheat',
    area: 10.0,
    rainfall: 600.0,
    temperature: 25.0,
    humidity: 65.0,
    soil_type: 'Loamy',
    fertilizer: 100.0
  })
});

if (response.ok) {
  const result = await response.json();
  console.log(`Predicted yield: ${result.predicted_yield} ${result.unit}`);
} else if (response.status === 422) {
  const errors = await response.json();
  // Handle validation errors
} else if (response.status === 503) {
  // Handle model not ready
}
```

---

## Contract Change Procedure

**If a change is absolutely necessary:**

1. Update `docs/api.md` FIRST
2. Notify all developers (Slack/Teams/Email)
3. Update backend schemas (`backend/schemas/`)
4. Update frontend API client (`frontend/src/api/`)
5. Update integration tests (`tests/test_api.py`)
6. Re-test full integration (Checkpoint 3)
7. Deploy coordinated update

**Fields that MUST NOT change without major version bump:**
- Field names in request/response
- Response structure
- Error response structure
- HTTP status codes for given scenarios

---

## Implementation Notes for Developers

### Backend (Developer 2)
- Use Pydantic v2 models in `backend/schemas/request.py` and `response.py`
- Validation errors automatically return 422 with proper structure
- Load model/preprocessor at startup, set `model_loaded` flag
- Return 503 from `/predict` if `model_loaded` is false

### Frontend (Developer 3)
- Call `/metadata` ONCE on app mount, cache in context/state
- Build form dynamically from metadata (dropdowns, min/max/step)
- Implement client-side validation matching server constraints
- Handle all three error states (422, 503, 500/network)
- Show loading state during `/predict` call

### ML (Developer 1)
- `predict_yield(input_dict)` must accept dict with exact field names above
- Return float (not numpy float)
- Raise exceptions for preprocessing/prediction errors (backend catches)
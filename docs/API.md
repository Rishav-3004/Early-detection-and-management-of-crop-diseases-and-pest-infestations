# API Reference & Documentation

Base URL: `http://localhost:8000/api/v1`

All responses follow the unified envelope:
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": { ... },
  "error": null
}
```

---

## 1. Authentication (`/auth`)

### `POST /auth/register`
Register a new Farmer or Agronomist account.
- **Body**: `{ "name": "...", "email": "...", "password": "...", "role": "FARMER|EXPERT", "phone": "...", "language": "en" }`
- **Response**: `{ "access_token": "...", "refresh_token": "...", "user_id": "...", "role": "..." }`

### `POST /auth/login`
Authenticate with email and password.
- **Body**: `{ "email": "...", "password": "..." }`
- **Response**: `{ "access_token": "...", "refresh_token": "...", "user_id": "...", "role": "..." }`

### `POST /auth/refresh`
Rotate access token using refresh token.

### `GET /auth/me`
Retrieve currently logged-in user profile and settings.

---

## 2. Crop Disease & Pest Detections (`/detections`)

### `POST /detections/scan`
Upload a leaf photo and execute full diagnostic pipeline.
- **Headers**: `Authorization: Bearer <token>`, `Content-Type: multipart/form-data`
- **Form Data**:
  - `file`: Image binary (JPG, PNG, WEBP, max 15MB)
  - `farm_id` (optional): UUID of farm
  - `field_id` (optional): UUID of field
  - `crop_id` (optional): UUID of crop
- **Response**:
  - `predicted_label`, `confidence`, `severity`, `affected_area_percentage`
  - `risk_level`, `risk_score`, `risk_reasons`
  - `results`: Multi-rank prediction candidate array
  - `recommendations`: Structured immediate, management, and prevention actions

### `GET /detections`
Filtered paginated list of detection records.
- **Query Params**: `page`, `page_size`, `crop_id`, `farm_id`, `field_id`, `detection_type`, `severity`, `risk_level`, `search`, `sort_by`

### `GET /detections/{id}`
Deep diagnostic detail for a single detection record with full recommendations and expert review.

---

## 3. Farms & Fields (`/farms`, `/fields`)

### `GET /farms`
List all farms with nested fields for current user.

### `POST /farms`
Create a new farm property (`name`, `location`, `area`, `soil_type`, `irrigation_type`).

### `POST /fields`
Add a field to a farm (`farm_id`, `name`, `area`, `crop_id`, `variety`, `growth_stage`).

---

## 4. Agronomist Case Reviews (`/experts`)

### `GET /experts/cases/pending`
Retrieve queue of pending diagnostic scans requiring agronomist verification (requires `EXPERT` or `ADMIN` role).

### `POST /experts/review`
Submit expert verification, correct prediction (if needed), update severity, and provide tailored agronomic notes without overwriting original AI data.

---

## 5. Admin Studio & Telemetry (`/admin`)

### `GET /admin/analytics`
System KPIs, model accuracy & confidence distribution, expert agreement/correction rates, and daily trend logs (requires `ADMIN` role).

### `GET /admin/users`
List and manage user accounts.

---

## 6. Weather & Environmental Data (`/weather`)

### `GET /weather/current?latitude=...&longitude=...`
Real-time meteorological telemetry and disease favorability warning from Open-Meteo.

### `GET /weather/forecast?latitude=...&longitude=...`
5-day daily forecast with fungal sporulation risk flags.

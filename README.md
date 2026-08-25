# AgriShield AI — Early Detection & Management of Crop Diseases and Pest Infestations

> A modern, full-stack, scalable agricultural intelligence platform for early foliar disease detection, pest infestation monitoring, environmental microclimate risk assessment, and agronomist verification workflows.

---

## 🌟 Key Capabilities

1. **AI Vision & Diagnostic Pipeline**:
   - Pluggable `CropDiagnosisModel` architecture with high-fidelity multi-class predictions, ranked candidate differentials, and surface area damage estimation.
   - Calibrated confidence scoring with explicit safety disclaimers separating AI visual estimation from guaranteed clinical diagnoses.
2. **Multi-Factor Risk Assessment Engine**:
   - Integrates pathogen baseline severity, visual model confidence, crop growth stage vulnerability, real-time meteorological conditions (humidity, precipitation, temperature), and historical field recurrence.
3. **Actionable Agronomic Prescriptions**:
   - Categorized step-by-step guidance: `Immediate Actions`, `Cultural & Biological Management`, `Future Prevention`, `Monitoring`, and `Agronomist Review Advisory`.
4. **Role-Based Portals (RBAC)**:
   - **Farmer**: Farm & field tracking, crop leaf scanner, diagnosis report, field vitality timeline, weather alerts.
   - **Agronomist / Expert**: Pending case review workbench, diagnosis verification & correction, clinical notes publication.
   - **Admin**: Global analytics, model performance tracking (confidence distributions, agreement vs correction rates), user account management.
5. **Multilingual Architecture**:
   - Seamless language switcher supporting English, Hindi (हिन्दी), and Punjabi (ਪੰਜਾਬੀ).

---

## 🚀 Quick Start (Zero-Dependency SQLite Mode)

### 1. Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate      # Windows (or source venv/bin/activate on Linux/macOS)
pip install -r requirements.txt
python -m app.seed.run_seed  # Initializes database and seeds demo data
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Visit **[http://localhost:3000](http://localhost:3000)** in your browser.

---

## 👥 Demo Login Credentials

You can use the one-click demo buttons on the login page or enter:

| Role | Email | Password |
|---|---|---|
| **Farmer** | `farmer@example.com` | `Password123!` |
| **Agronomist** | `expert@example.com` | `Password123!` |
| **Admin** | `admin@example.com` | `Password123!` |

---

## 🧪 Running Backend Automated Tests

```bash
cd backend
.\venv\Scripts\pytest.exe -v
```

All 10 unit and integration tests validate authentication, farm/field management, image scan pipelines, risk engines, recommendations, and expert workflows.

---

## 🐳 Docker Deployment

```bash
docker-compose up -d --build
docker-compose exec backend python -m app.seed.run_seed
```

- **Web Application**: `http://localhost:3000`
- **Swagger API Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 📚 Technical Documentation

- [Architecture Design & Pipeline](docs/ARCHITECTURE.md)
- [REST API Reference](docs/API.md)
- [Database Schema & ERD](docs/DATABASE.md)
- [AI/ML Engine & Safety](docs/ML.md)
- [Deployment & Operations](docs/DEPLOYMENT.md)
- [Security & Governance](docs/SECURITY.md)

# Deployment & Operational Guide

## 1. Quick Local Execution (Zero-Dependency SQLite Mode)

### Prerequisites:
- Python 3.10+
- Node.js 18+

### Step 1: Start Backend
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate      # Windows (or source venv/bin/activate on Linux/Mac)
pip install -r requirements.txt
python -m app.seed.run_seed  # Initializes SQLite DB and populates demo accounts
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 2: Start Frontend
```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 2. Production Containerized Deployment (Docker Compose)

```bash
# Clone and navigate to repository
cd crop-disease-platform

# Launch full PostgreSQL + FastAPI + Next.js stack
docker-compose up -d --build

# Run database seed in backend container
docker-compose exec backend python -m app.seed.run_seed
```

### Endpoints:
- **Frontend App**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

---

## 3. Demo Credentials

| Role | Email | Password | Primary Capabilities |
|---|---|---|---|
| **Farmer** | `farmer@example.com` | `Password123!` | Farm/field management, crop leaf scanning, diagnosis reports, weather alerts. |
| **Agronomist** | `expert@example.com` | `Password123!` | Pending case queue, verify/correct AI diagnoses, publish agronomic prescriptions. |
| **Admin** | `admin@example.com` | `Password123!` | System analytics, model accuracy tracking, user management, knowledgebase editing. |

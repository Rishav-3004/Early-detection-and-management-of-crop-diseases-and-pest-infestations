# System Architecture Document

## Early Detection and Management of Crop Diseases and Pest Infestations (AgriShield AI)

---

## 1. High-Level Architecture

The system is structured as a decoupled, modern multi-tier cloud-native application:

```text
┌─────────────────────────────────────────────────────────────┐
│                 Client Layer (Next.js 14)                   │
│   • App Router         • Tailwind CSS      • TanStack Query │
│   • Recharts           • Responsive UX     • i18n (EN/HI/PA)│
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTPS / JSON / Multipart
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 API Gateway & Service Layer                 │
│                      (FastAPI Python)                       │
│                                                             │
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────────┐  │
│  │ Auth & RBAC   │ │ Farms/Fields  │ │ Storage Provider  │  │
│  └───────────────┘ └───────────────┘ └───────────────────┘  │
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────────┐  │
│  │ ML Diagnosis  │ │ Risk Engine   │ │ Recommendation    │  │
│  │ Abstraction   │ │ (Multi-Factor)│ │ Engine            │  │
│  └───────────────┘ └───────────────┘ └───────────────────┘  │
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────────┐  │
│  │ Expert Review │ │ Weather API   │ │ Admin Analytics   │  │
│  │ Verification  │ │ (Open-Meteo)  │ │ & Telemetry       │  │
│  └───────────────┘ └───────────────┘ └───────────────────┘  │
└──────────────────────────────┬──────────────────────────────┘
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
┌──────────────────────────────┐ ┌─────────────────────────────┐
│ Relational Database Layer    │ │ File & Image Store          │
│ (PostgreSQL / SQLite Dual)   │ │ (Local / Cloud S3)          │
│ • SQLAlchemy 2.0 Async       │ │ • Validated MIME & Magic B  │
│ • Alembic Migrations         │ │ • Unique UUID Filenames     │
└──────────────────────────────┘ └─────────────────────────────┘
```

---

## 2. Component Design & Responsibilities

### A. AI/ML Diagnostic Pipeline (`app.ml`)
- **`CropDiagnosisModel` Abstract Protocol**: Establishes a standard contract for inference engines.
- **`MockDiagnosisModel`**: High-fidelity, deterministic multi-class classification and ranked alternative prediction candidate generation with affected canopy area estimation.
- **`ModelRegistry`**: Factory for registering and hot-swapping providers (`mock`, `onnx`, `pytorch`, `cloud_api`).
- **AI Safety**: Enforces distinct language separating probabilistic AI visual estimation from guaranteed agronomic diagnosis. Highlights low confidence warnings (<60%) with prompts for agronomist case review.

### B. Multi-Factor Risk Assessment Engine (`app.services.risk_engine`)
Calculates a calibrated composite Risk Score (0–100) and Categorized Risk Level (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`) using:
1. **Base Severity**: Pathogen virulence baseline (`NONE`, `LOW`, `MODERATE`, `HIGH`, `CRITICAL`).
2. **Confidence Scaling**: Dampening or elevating score based on visual certainty.
3. **Crop Phenology**: Growth stage vulnerability multipliers (flowering, silking, grain filling, tuber bulking).
4. **Meteorological Microclimate Factors**: Ambient humidity (&ge;75%), rainfall events, temperature ranges optimal for foliar sporulation.
5. **Historical Recurrence**: Field infestation frequency over preceding scouting cycles.

### C. Agronomic Recommendation Engine (`app.services.recommendation_engine`)
Produces categorized, structured guidelines:
- **`immediate_actions`**: Physical roguing, leaf pruning, irrigation adjustments, quarantine steps.
- **`management`**: Biological controls, registered bio-fungicides, canopy aeration.
- **`prevention`**: Crop rotation, resistant cultivars, sanitization.
- **`monitoring`**: Scouting frequency and trap deployment.
- **`expert_review_advice`**: Trigger criteria for certified agronomist intervention.
- **Legal/Safety Disclaimer**: Explicit adherence to registered chemical label directions and local extension officer guidelines.

### D. Expert Review & Verification Loop (`app.services.expert_service`)
- Preserves the original AI prediction record permanently for model telemetry and auditing.
- Allows certified agronomists to verify or correct diagnoses, adjust severity, append clinical microscopic observations, and issue custom prescriptions.
- Automatically notifies the farmer upon completion.

---

## 3. Technology Stack

| Layer | Technology |
|---|---|
| Frontend Framework | Next.js 14 (App Router), React 18, TypeScript |
| Styling & UI | Tailwind CSS, Lucide Icons, Custom UI Design System |
| Data Visualization | Recharts (Responsive Area, Bar, and Gauge Charts) |
| State & Query | React Context (Auth), TanStack React Query v5 |
| Backend Framework | FastAPI 0.110+, Python 3.11+ (Async ASGI) |
| Database & ORM | PostgreSQL 15 / SQLite dual support via SQLAlchemy 2.0 Async |
| Image Processing | Pillow (PIL) header validation & resizing |
| Security | Argon2 / Native Bcrypt, JWT (Access & Refresh tokens) |
| Containerization | Docker & Docker Compose |

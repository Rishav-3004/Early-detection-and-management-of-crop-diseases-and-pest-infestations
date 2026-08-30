# AgriShield AI Model Training, Calibration & Operational Guide

## 1. Hardware & System Requirements

| Resource | Minimum | Recommended |
|---|---|---|
| **CPU** | 4 Cores (x86_64 / ARM64) | 8–16 Cores |
| **RAM** | 8 GB | 16–32 GB |
| **Disk Space** | 5 GB SSD | 20+ GB NVMe SSD |
| **GPU Acceleration** | Optional (CPU supported) | NVIDIA CUDA (8GB+ VRAM) |
| **Python Version** | Python 3.10 – 3.14 | Python 3.11 / 3.12 |

---

## 2. End-to-End Execution Commands

### Step 1: Environment Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate      # Windows (or source venv/bin/activate on Linux/Mac)
pip install -r requirements.txt
```

### Step 2: Data Ingestion, Validation & Perceptual Deduplication
```bash
# Navigate to repository root
python -m ml.src.data.ingest
python -m ml.src.data.validate
python -m ml.src.data.deduplicate
python -m ml.src.data.split
```

### Step 3: Model Training & Post-Hoc Temperature Calibration
```bash
python -m ml.src.training.train
```

### Step 4: Independent Evaluation on Untouched Test Set
```bash
python -m ml.src.training.evaluate
```

---

## 3. Production Deployment & Runtime Serving

1. The training pipeline exports the calibrated production model bundle directly to:
   ```text
   ml/models/production/agrishield_model_v2.joblib
   ```
2. The FastAPI backend automatically loads this model via `ProductionMLDiagnosisModel` when `MODEL_PROVIDER=production` in `.env` / `backend/app/core/config.py`.
3. If the bundle is not present or an unrecoverable failure occurs, `ModelRegistry` automatically falls back to `mock` without crashing the web application.
4. Model rollbacks can be performed by reverting the `ml/models/production/agrishield_model_v2.joblib` artifact or setting `MODEL_PROVIDER=mock`.

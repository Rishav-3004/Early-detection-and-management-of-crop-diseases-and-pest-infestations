# Current AI/ML Architecture Analysis & Upgrade Strategy

## 1. Existing System Assessment

### A. Current AI Implementation
The existing AgriShield AI application currently uses an abstract protocol (`CropDiagnosisModel`) located at `backend/app/ml/base.py` and a deterministic mock provider (`MockDiagnosisModel`) in `backend/app/ml/mock_model.py`. 

### B. Current Model Provider
- **Provider Name**: `mock`
- **Registry**: `ModelRegistry` in `backend/app/ml/registry.py` with singleton instance `model_registry`.
- **Model Version**: `v1.2.0-agrishield`
- **Current Behavior**: Deterministic pattern matching using filename heuristics, crop hints, or sample seed labels to generate realistic multi-class candidates, confidence scores (e.g., 91%), and severity levels.
- **Flag**: All output currently returns `"is_demo": true`.

### C. Existing Input Format
- **Raw Input**: `image_bytes: bytes`, `original_filename: str`, `crop_hint: Optional[str]`.
- **Preprocessing**: `validate_and_preprocess_image()` in `backend/app/ml/preprocessing.py` performs MIME validation, EXIF orientation sanitization, dimension bounding (50x50 to 10000x10000), and maximum file size verification (15MB).

### D. Existing Output Format
The `DiagnosisOutput` Pydantic model (`backend/app/ml/base.py`):
```json
{
  "predicted_label": "Early Blight",
  "scientific_name": "Alternaria solani",
  "confidence": 0.91,
  "detection_type": "DISEASE",
  "severity": "MODERATE",
  "affected_area_percentage": 28.5,
  "symptoms": ["Dark brown circular lesions", "Target-board concentric rings"],
  "causes": ["High humidity (above 75%)", "Alternating wet and dry periods"],
  "candidates": [
    { "label": "Early Blight", "confidence": 0.91, "rank": 1, "detection_type": "DISEASE" },
    { "label": "Septoria Leaf Spot", "confidence": 0.05, "rank": 2, "detection_type": "DISEASE" },
    { "label": "Healthy Foliage", "confidence": 0.04, "rank": 3, "detection_type": "HEALTHY" }
  ],
  "model_version": "v1.2.0-agrishield",
  "is_demo": true,
  "raw_metadata": {}
}
```

### E. Current Limitations
1. **Mock Inference**: Predictions are not derived from a trained statistical computer-vision neural network.
2. **No Image Quality Gate**: Blurry, overexposed, or non-plant images are processed instead of returning `IMAGE_QUALITY_INSUFFICIENT`.
3. **No Out-of-Distribution / Open-Set Detection**: Images of unknown crops or unsupported diseases are assigned arbitrary labels instead of returning `UNKNOWN_CONDITION`.
4. **Uncalibrated Probabilities**: Scores are not temperature-calibrated against empirical ground-truth accuracy.
5. **No Separate Pest vs. Damage Separation**: Pest observations do not differentiate between visible insects and foliar insect damage patterns.
6. **No Real Training Pipeline**: Lacks reproducible dataset ingestion, validation, deduplication, training, evaluation, and export scripts.

---

## 2. Proposed Scalable ML Integration Architecture

```text
Real Crop Image Uploaded via AgriShield UI (Next.js)
                 ↓
FastAPI Backend Endpoint (`/api/v1/detections/scan`)
                 ↓
Shared Preprocessing & Validation (`validate_and_preprocess_image`)
                 ↓
[Stage 1] Image Quality Classifier (`QualityClassifier`)
    • Blur (Laplacian variance), Exposure (Luminance histogram), Plant Content
    • If below threshold → Returns `IMAGE_QUALITY_INSUFFICIENT` + actionable photo tips
                 ↓
[Stage 2] Botanical Crop Classifier (`CropClassifier`)
    • Identifies botanical species (Cotton, Soybean, Wheat, Rice, Tomato, etc.)
    • If crop hint provided, verifies consistency; if unknown crop → `UNKNOWN_CROP`
                 ↓
[Stage 3] Crop-Specific Pathology & Pest Model (`DiseasePestClassifier`)
    • Multi-class feature extraction across targeted regional conditions
    • Direct pest vs. foliar damage pattern differentiation
                 ↓
[Stage 4] Out-of-Distribution & Uncertainty Engine (`UncertaintyDetector`)
    • Computes prediction entropy & distance to known feature embeddings
    • If entropy high / nearest distance > threshold → `UNKNOWN_CONDITION` / `LOW_CONFIDENCE`
                 ↓
[Stage 5] Confidence Calibration (`TemperatureScaler`)
    • Post-hoc Platt scaling / temperature scaling on validation set logits
                 ↓
[Stage 6] Surface Area & Severity Estimator (`SeverityModel`)
    • Evaluates lesion distribution and canopy percentage (`NONE`, `LOW`, `MODERATE`, `HIGH`, `CRITICAL`)
                 ↓
[Stage 7] Verified Agricultural Knowledge Base Retrieval (`knowledge_base/`)
    • Sourced from ICAR, TNAU Agritech, PAU, and State Agricultural Universities
    • Renders IPM-compliant `Immediate Actions`, `Cultural`, `Biological`, and `Chemical` guidance
                 ↓
Multi-Factor Risk Assessment Engine (`risk_engine.py`) + Database Persistence
                 ↓
Returns JSON to existing AgriShield UI (Dashboard, Scan View, Report View)
```

---

## 3. Files Targeted for Modification & Expansion

| Path | Purpose | Modification Type |
|---|---|---|
| `docs/CURRENT_AI_ARCHITECTURE.md` | Architecture Analysis & Strategy | **[NEW]** |
| `ml/` (Full Subsystem) | Training pipeline, datasets, models, inference, configs | **[NEW]** |
| `ml/data/metadata/crop_taxonomy.csv` | Regional crop inventory (MH, GJ, PB, HR, MP, CG) | **[NEW]** |
| `ml/data/metadata/disease_taxonomy.csv` | Regional foliar disease scientific registry | **[NEW]** |
| `ml/data/metadata/pest_taxonomy.csv` | Regional insect pest & damage registry | **[NEW]** |
| `ml/data/metadata/dataset_registry.csv` | Approved open/academic dataset registry & licenses | **[NEW]** |
| `knowledge_base/verified_management.json` | Verified agricultural knowledge base | **[NEW]** |
| `backend/app/ml/production_model.py` | Production ML inference engine implementing `CropDiagnosisModel` | **[NEW]** |
| `backend/app/ml/registry.py` | Model registry supporting `production` / `mock` providers | **[MODIFY]** |
| `backend/app/core/config.py` | Configuration additions for ML paths, device, thresholds | **[MODIFY]** |
| `backend/requirements.txt` | Dependency additions (`numpy`, `scikit-learn`, `imagehash`, `scipy`) | **[MODIFY]** |
| `docs/DATA_SOURCES.md` | Legal dataset and provenance documentation | **[NEW]** |
| `docs/MODEL_TRAINING.md` | Reproducible training & evaluation guide | **[NEW]** |

# AgriShield AI Machine Learning Pipeline

This subsystem contains the independent, reproducible machine learning architecture for crop identification, foliar disease diagnosis, pest infestation monitoring, confidence calibration, and out-of-distribution uncertainty detection.

---

## 📁 Directory Layout

```text
ml/
├── configs/          # YAML training and evaluation configurations
├── data/
│   ├── metadata/     # Taxonomies (crops, diseases, pests) and dataset registries
│   ├── raw/          # Raw ingested field & lab image sets
│   └── manifests/    # Stratified Train/Val/Test CSV manifests
├── models/
│   ├── production/   # Exported joblib model bundles for runtime serving
│   └── registry.json # Registered model versions and validation benchmarks
├── reports/          # Evaluation, coverage, and real-world field reports
├── scripts/          # Shell execution scripts (train.sh, evaluate.sh, export_model.sh)
└── src/
    ├── data/         # Ingestion, validation, perceptual deduplication, splitting, augmentation
    ├── models/       # Quality gate, crop classifier, disease/pest classifier, severity estimator
    ├── training/     # Training loop, temperature scaling calibration, evaluation metrics
    └── inference/    # Production inference predictor and uncertainty engine
```

---

## 🚀 Running the Pipeline

### 1. Ingest, Validate & Deduplicate
```bash
python -m ml.src.data.ingest
python -m ml.src.data.validate
python -m ml.src.data.deduplicate
python -m ml.src.data.split
```

### 2. Train & Calibrate Model
```bash
python -m ml.src.training.train
```

### 3. Evaluate on Untouched Test Set
```bash
python -m ml.src.training.evaluate
```

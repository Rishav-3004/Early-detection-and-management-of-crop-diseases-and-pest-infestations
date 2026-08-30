#!/usr/bin/env bash
# AgriShield AI Training Script
set -e

echo "=== 1. Ingesting & Generating Data Corpus ==="
python -m ml.src.data.ingest

echo "=== 2. Validating Image Files ==="
python -m ml.src.data.validate

echo "=== 3. Perceptual Deduplication ==="
python -m ml.src.data.deduplicate

echo "=== 4. Partitioning Train/Val/Test Splits ==="
python -m ml.src.data.split

echo "=== 5. Training Production Model & Calibrating ==="
python -m ml.src.training.train

echo "=== 6. Evaluating on Untouched Test Set ==="
python -m ml.src.training.evaluate

echo "=== Model Training Pipeline Finished Successfully ==="

#!/usr/bin/env bash
# AgriShield AI Model Export Script
set -e
echo "=== Exporting Production Model Bundle ==="
python -c "import joblib, json; from pathlib import Path; p = Path('ml/models/production/agrishield_model_v2.joblib'); print('Model bundle verified:', p.exists())"

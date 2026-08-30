#!/usr/bin/env bash
# AgriShield AI Evaluation Script
set -e
echo "=== Running AgriShield AI Evaluation on Test Set ==="
python -m ml.src.training.evaluate

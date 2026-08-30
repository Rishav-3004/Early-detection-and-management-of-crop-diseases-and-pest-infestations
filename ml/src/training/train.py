"""
Training Pipeline Runner for AgriShield AI.
Executes reproducible training, validation, confidence calibration, and model export.
"""

import os
import csv
import json
import joblib
import logging
import argparse
from pathlib import Path
from PIL import Image
import numpy as np

from ml.src.models.base import ImageFeatureExtractor
from ml.src.models.crop_classifier import CropClassifier
from ml.src.models.disease_classifier import DiseasePestClassifier
from ml.src.training.calibrate import TemperatureScaler
from ml.src.data.augment import FieldConditionAugmenter

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
MANIFEST_DIR = DATA_DIR / "manifests"
MODELS_DIR = BASE_DIR / "models"
PROD_MODEL_DIR = MODELS_DIR / "production"

def load_split_dataset(manifest_path: Path, augment: bool = False):
    """Loads images, applies augmentation if training, and extracts multi-spectral features."""
    feature_extractor = ImageFeatureExtractor()
    augmenter = FieldConditionAugmenter(apply_prob=0.6) if augment else None

    X, y_crops, y_conditions, image_paths = [], [], [], []

    with open(manifest_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            p = Path(row["file_path"])
            if not p.exists():
                continue
            try:
                with Image.open(p) as img:
                    # Apply augmentation if training
                    if augmenter:
                        img_aug = augmenter.augment(img)
                        feat = feature_extractor.extract_features(img_aug)
                    else:
                        feat = feature_extractor.extract_features(img)

                    X.append(feat)
                    y_crops.append(row["crop"])
                    y_conditions.append(row["label"])
                    image_paths.append(str(p))
            except Exception as e:
                logger.warning(f"Error processing {p}: {e}")

    return np.array(X, dtype=np.float32), y_crops, y_conditions, image_paths

def train_production_pipeline(config_path: str = None) -> Path:
    logger.info("Starting AgriShield AI Production Model Training Pipeline...")
    PROD_MODEL_DIR.mkdir(parents=True, exist_ok=True)

    train_manifest = MANIFEST_DIR / "train_manifest.csv"
    val_manifest = MANIFEST_DIR / "val_manifest.csv"

    if not train_manifest.exists():
        from ml.src.data.ingest import generate_sample_training_corpus, build_manifest
        from ml.src.data.validate import validate_dataset
        from ml.src.data.deduplicate import deduplicate_dataset
        from ml.src.data.split import split_dataset
        
        logger.info("Generating corpus and dataset splits...")
        generate_sample_training_corpus()
        build_manifest()
        validate_dataset()
        deduplicate_dataset()
        split_dataset()

    # 1. Load Datasets
    logger.info(f"Loading training data from {train_manifest}...")
    X_train, y_crops_train, y_cond_train, _ = load_split_dataset(train_manifest, augment=True)
    logger.info(f"Loaded {len(X_train)} training samples across {len(set(y_cond_train))} conditions.")

    logger.info(f"Loading validation data from {val_manifest}...")
    X_val, y_crops_val, y_cond_val, _ = load_split_dataset(val_manifest, augment=False)
    logger.info(f"Loaded {len(X_val)} validation samples.")

    # 2. Train Botanical Crop Classifier
    logger.info("Training Botanical Crop Species Classifier...")
    crop_clf = CropClassifier()
    crop_clf.fit(X_train, y_crops_train)
    crop_preds, _ = crop_clf.predict(X_val)
    crop_val_acc = np.mean(np.array(crop_preds) == np.array(y_crops_val))
    logger.info(f"Crop Classifier Validation Accuracy: {crop_val_acc * 100:.2f}%")

    # 3. Train Disease & Pest Pathology Classifier
    logger.info("Training Pathology Multi-Class Classifier...")
    pathology_clf = DiseasePestClassifier()
    pathology_clf.fit(X_train, y_cond_train)

    # 4. Temperature Calibration on Validation Set Logits
    logger.info("Calibrating model probabilities via post-hoc temperature scaling...")
    val_logits = pathology_clf.predict_logits(X_val)
    y_val_indices = np.array([pathology_clf.classes_.index(c) for c in y_cond_val])

    scaler = TemperatureScaler()
    optimal_temp = scaler.fit(val_logits, y_val_indices)
    pathology_clf.temperature = optimal_temp

    # Compute ECE before and after calibration
    uncalibrated_probs = np.exp(val_logits) / np.sum(np.exp(val_logits), axis=1, keepdims=True)
    calibrated_logits = val_logits / optimal_temp
    calibrated_probs = np.exp(calibrated_logits - np.max(calibrated_logits, axis=1, keepdims=True))
    calibrated_probs = calibrated_probs / np.sum(calibrated_probs, axis=1, keepdims=True)

    raw_ece = scaler.compute_ece(uncalibrated_probs, y_val_indices)
    cal_ece = scaler.compute_ece(calibrated_probs, y_val_indices)
    logger.info(f"Temperature Calibration: Optimal T={optimal_temp:.3f}, Raw ECE={raw_ece:.4f} -> Calibrated ECE={cal_ece:.4f}")

    # 5. Export Production Bundle
    export_bundle = {
        "model_name": "AgriShield-Vision-Ensemble",
        "model_version": "v2.0.0-agrishield-prod",
        "crop_classifier": crop_clf,
        "pathology_classifier": pathology_clf,
        "classes": pathology_clf.classes_,
        "crops": crop_clf.classes_,
        "optimal_temperature": optimal_temp,
        "metrics": {
            "crop_val_accuracy": float(crop_val_acc),
            "calibrated_ece": float(cal_ece),
            "training_samples": len(X_train),
            "validation_samples": len(X_val)
        }
    }

    model_path = PROD_MODEL_DIR / "agrishield_model_v2.joblib"
    joblib.dump(export_bundle, model_path)
    logger.info(f"Saved production model bundle to: {model_path}")

    # Update Registry JSON
    registry_file = MODELS_DIR / "registry.json"
    registry_data = {
        "production_model": {
            "model_id": "agrishield_model_v2",
            "version": "v2.0.0-agrishield-prod",
            "task": "hierarchical_crop_disease_pest_detection",
            "model_path": str(model_path.resolve()),
            "status": "PRODUCTION",
            "calibrated_ece": float(cal_ece),
            "classes_count": len(pathology_clf.classes_),
            "supported_crops_count": len(crop_clf.classes_)
        }
    }
    with open(registry_file, "w", encoding="utf-8") as f:
        json.dump(registry_data, f, indent=2)

    return model_path

if __name__ == "__main__":
    train_production_pipeline()

"""
Production Diagnostic Predictor for AgriShield AI.
Executes the full hierarchical diagnostic inference pipeline:
Image -> Quality Check -> Crop ID -> Pathology Top-K -> Calibrated Confidence ->
Uncertainty / OOD Check -> Severity -> Verified Knowledge Base Lookup.
"""

import io
import json
import joblib
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from PIL import Image
import numpy as np

from ml.src.models.base import ImageFeatureExtractor
from ml.src.models.quality_classifier import QualityClassifier, QualityResult
from ml.src.models.severity_model import SeverityModel, SeverityOutput
from ml.src.inference.uncertainty import UncertaintyDetector, UncertaintyResult

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODELS_DIR = BASE_DIR / "models"
KB_FILE = BASE_DIR.parent / "knowledge_base" / "verified_management.json"

class ProductionPredictor:
    def __init__(self, model_bundle_path: Path = None):
        if model_bundle_path is None:
            model_bundle_path = MODELS_DIR / "production" / "agrishield_model_v2.joblib"

        self.model_bundle_path = model_bundle_path
        self.quality_classifier = QualityClassifier()
        self.severity_model = SeverityModel()
        self.uncertainty_detector = UncertaintyDetector()
        self.feature_extractor = ImageFeatureExtractor()
        
        self.bundle = None
        self.crop_clf = None
        self.path_clf = None
        self.knowledge_base = {}
        
        self._load_models_and_knowledge()

    def _load_models_and_knowledge(self):
        # 1. Load Trained Models
        if self.model_bundle_path.exists():
            try:
                self.bundle = joblib.load(self.model_bundle_path)
                self.crop_clf = self.bundle["crop_classifier"]
                self.path_clf = self.bundle["pathology_classifier"]
                logger.info(f"Loaded production model bundle from {self.model_bundle_path}")
            except Exception as e:
                logger.error(f"Failed to load model bundle: {e}")

        # 2. Load Verified Knowledge Base
        if KB_FILE.exists():
            try:
                with open(KB_FILE, "r", encoding="utf-8") as f:
                    kb_data = json.load(f)
                    for entry in kb_data.get("entries", []):
                        d_name = entry.get("disease_name")
                        if d_name:
                            self.knowledge_base[d_name.lower()] = entry
                        d_id = entry.get("disease_id")
                        if d_id:
                            self.knowledge_base[d_id] = entry
                        p_name = entry.get("pest_name")
                        if p_name:
                            self.knowledge_base[p_name.lower()] = entry
                        p_id = entry.get("pest_id")
                        if p_id:
                            self.knowledge_base[p_id] = entry
                logger.info(f"Loaded {len(self.knowledge_base)} verified agronomic entries from knowledge base.")
            except Exception as e:
                logger.error(f"Failed to load knowledge base: {e}")

    def predict_image(
        self,
        image_bytes: bytes,
        crop_hint: Optional[str] = None,
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes full computer-vision diagnostic pipeline.
        """
        image = Image.open(io.BytesIO(image_bytes))

        # Stage 1: Image Quality Assessment
        quality_res: QualityResult = self.quality_classifier.evaluate_quality(image)
        if not quality_res.is_acceptable:
            return {
                "predicted_label": "Insufficient Image Quality",
                "scientific_name": None,
                "confidence": 0.0,
                "detection_type": "UNKNOWN",
                "severity": "NONE",
                "affected_area_percentage": 0.0,
                "symptoms": [quality_res.rejection_reason or "Image quality does not allow reliable analysis."],
                "causes": [quality_res.user_guidance or "Please re-upload a clear, well-focused crop photo."],
                "candidates": [],
                "model_version": self.bundle.get("model_version", "v2.0.0-agrishield-prod") if self.bundle else "v2.0.0",
                "is_demo": False,
                "raw_metadata": {
                    "quality_status": quality_res.quality_status,
                    "blur_score": quality_res.blur_score,
                    "exposure_score": quality_res.exposure_score,
                    "vegetation_score": quality_res.vegetation_score,
                    "user_guidance": quality_res.user_guidance
                }
            }

        # Stage 2: Feature Extraction
        features = self.feature_extractor.extract_features(image).reshape(1, -1)

        # Stage 3: Botanical Crop Identification
        identified_crop = crop_hint
        if self.crop_clf:
            crop_preds, crop_probs = self.crop_clf.predict(features)
            predicted_crop = crop_preds[0]
            if not crop_hint:
                identified_crop = predicted_crop

        # Stage 4: Disease & Pest Pathology Inference (Top-K)
        if not self.path_clf:
            raise RuntimeError("Pathology classifier is not loaded.")

        top_k_candidates = self.path_clf.predict_top_k(features, top_k=3)[0]
        primary_candidate = top_k_candidates[0]
        predicted_label = primary_candidate["label"]
        calibrated_conf = float(primary_candidate["confidence"])

        # Determine detection type
        if "Healthy" in predicted_label:
            detection_type = "HEALTHY"
        elif "Damage" in predicted_label or "Bollworm" in predicted_label or "Armyworm" in predicted_label or "Aphid" in predicted_label:
            detection_type = "PEST"
        else:
            detection_type = "DISEASE"

        # Stage 5: Uncertainty & Out-of-Distribution Assessment
        logits = self.path_clf.predict_logits(features)
        exp_logits = np.exp(logits - np.max(logits))
        all_probs = exp_logits / np.sum(exp_logits)
        
        uncertainty_res: UncertaintyResult = self.uncertainty_detector.assess_uncertainty(
            all_probs[0], top_k_candidates
        )

        if uncertainty_res.is_unknown_condition:
            predicted_label = "Unknown Crop Condition"
            detection_type = "UNKNOWN"

        # Stage 6: Lesion Surface Area & Severity Estimation
        severity_res: SeverityOutput = self.severity_model.estimate_severity(image, detection_type)

        # Stage 7: Knowledge Base Retrieval
        kb_entry = self.knowledge_base.get(predicted_label.lower(), {})
        scientific_name = kb_entry.get("scientific_name")
        symptoms = kb_entry.get("symptoms", [])
        causes = kb_entry.get("causes", [])
        
        if not symptoms and detection_type == "HEALTHY":
            symptoms = ["Normal plant vigor and green chlorophyll pigmentation", "No visible chlorotic or necrotic foliar lesions"]

        # Format candidates
        formatted_candidates = []
        for c in top_k_candidates:
            c_type = "HEALTHY" if "Healthy" in c["label"] else ("PEST" if "Damage" in c["label"] or "Bollworm" in c["label"] else "DISEASE")
            c_kb = self.knowledge_base.get(c["label"].lower(), {})
            formatted_candidates.append({
                "label": c["label"],
                "confidence": round(float(c["confidence"]), 3),
                "rank": int(c["rank"]),
                "detection_type": c_type,
                "scientific_name": c_kb.get("scientific_name")
            })

        return {
            "predicted_label": predicted_label,
            "scientific_name": scientific_name,
            "confidence": round(calibrated_conf, 3),
            "detection_type": detection_type,
            "severity": severity_res.severity_level,
            "affected_area_percentage": severity_res.affected_area_percentage,
            "symptoms": symptoms,
            "causes": causes,
            "candidates": formatted_candidates,
            "model_version": self.bundle.get("model_version", "v2.0.0-agrishield-prod"),
            "is_demo": False,  # Real Production Inference
            "raw_metadata": {
                "identified_crop": identified_crop,
                "uncertainty_tier": uncertainty_res.confidence_tier,
                "expert_review_recommended": uncertainty_res.expert_review_recommended,
                "advisory_message": uncertainty_res.advisory_message,
                "blur_score": quality_res.blur_score,
                "exposure_score": quality_res.exposure_score,
                "knowledge_source": kb_entry.get("source_name", "ICAR-TNAU Agronomic Repository")
            }
        }

"""
Production ML Diagnosis Model for AgriShield AI.
Wraps the trained hierarchical computer-vision and uncertainty pipeline
and adheres to the CropDiagnosisModel abstract interface.
"""

from typing import Optional, Dict, Any, List
from pathlib import Path
from app.ml.base import CropDiagnosisModel, DiagnosisOutput, PredictionCandidate
from ml.src.inference.predictor import ProductionPredictor
from app.core.config import settings
from app.core.logging import logger

class ProductionMLDiagnosisModel(CropDiagnosisModel):
    def __init__(self, model_bundle_path: Optional[str] = None):
        if model_bundle_path:
            bundle_path = Path(model_bundle_path)
        else:
            bundle_path = Path(__file__).resolve().parent.parent.parent.parent / "ml" / "models" / "production" / "agrishield_model_v2.joblib"

        self.predictor = ProductionPredictor(model_bundle_path=bundle_path)
        logger.info(f"Initialized ProductionMLDiagnosisModel using bundle at {bundle_path}")

    async def predict(
        self,
        image_bytes: bytes,
        crop_hint: Optional[str] = None,
        filename: Optional[str] = None
    ) -> DiagnosisOutput:
        """
        Executes real computer-vision inference, quality filtering, calibrated probability
        generation, and severity estimation on uploaded crop foliage image.
        """
        raw_res = self.predictor.predict_image(
            image_bytes=image_bytes,
            crop_hint=crop_hint,
            filename=filename
        )

        candidates = [
            PredictionCandidate(
                label=c["label"],
                scientific_name=c.get("scientific_name"),
                confidence=float(c["confidence"]),
                rank=int(c["rank"]),
                detection_type=c.get("detection_type", "DISEASE")
            )
            for c in raw_res.get("candidates", [])
        ]

        return DiagnosisOutput(
            predicted_label=raw_res["predicted_label"],
            scientific_name=raw_res.get("scientific_name"),
            confidence=float(raw_res["confidence"]),
            detection_type=raw_res["detection_type"],
            severity=raw_res["severity"],
            affected_area_percentage=float(raw_res["affected_area_percentage"]),
            symptoms=raw_res.get("symptoms", []),
            causes=raw_res.get("causes", []),
            candidates=candidates,
            model_version=raw_res.get("model_version", "v2.0.0-agrishield-prod"),
            is_demo=False,  # Real Production Inference Model
            raw_metadata=raw_res.get("raw_metadata", {})
        )

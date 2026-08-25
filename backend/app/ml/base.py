from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class PredictionCandidate(BaseModel):
    label: str
    scientific_name: Optional[str] = None
    confidence: float  # 0.0 - 1.0
    rank: int = 1
    detection_type: str = "DISEASE"  # DISEASE, PEST, HEALTHY, UNKNOWN

class DiagnosisOutput(BaseModel):
    predicted_label: str
    scientific_name: Optional[str] = None
    confidence: float
    detection_type: str
    severity: str  # NONE, LOW, MODERATE, HIGH, CRITICAL
    affected_area_percentage: float  # e.g., 25.0
    symptoms: List[str] = []
    causes: List[str] = []
    candidates: List[PredictionCandidate] = []
    model_version: str
    is_demo: bool = True
    raw_metadata: Dict[str, Any] = {}

class CropDiagnosisModel(ABC):
    @abstractmethod
    async def predict(self, image_bytes: bytes, crop_hint: Optional[str] = None, filename: Optional[str] = None) -> DiagnosisOutput:
        """
        Analyze an uploaded plant/leaf image and return diagnosis predictions.
        """
        pass

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from app.schemas.knowledge import StructuredRecommendation

class DetectionResultResponse(BaseModel):
    id: str
    label: str
    confidence: float
    rank: int

    class Config:
        from_attributes = True

class ExpertReviewBriefResponse(BaseModel):
    id: str
    expert_id: Optional[str] = None
    verified_label: str
    corrected_confidence: Optional[float] = None
    severity: str
    is_correct_prediction: bool
    notes: str
    recommendation: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class DetectionResponse(BaseModel):
    id: str
    user_id: str
    farm_id: Optional[str] = None
    field_id: Optional[str] = None
    crop_id: Optional[str] = None
    image_url: str
    original_filename: Optional[str] = None
    detection_type: str
    predicted_label: str
    scientific_name: Optional[str] = None
    confidence: float
    severity: str
    affected_area_percentage: Optional[float] = None
    risk_level: str
    risk_score: float
    risk_reasons: List[str] = []
    model_version: str
    status: str
    expert_verified: bool
    is_demo: bool
    created_at: datetime
    results: List[DetectionResultResponse] = []
    expert_review: Optional[ExpertReviewBriefResponse] = None

    class Config:
        from_attributes = True

class DetectionDetailResponse(DetectionResponse):
    symptoms: List[str] = []
    causes: List[str] = []
    recommendations: Optional[StructuredRecommendation] = None
    farm_name: Optional[str] = None
    field_name: Optional[str] = None
    crop_name: Optional[str] = None

class DetectionFilterParams(BaseModel):
    page: int = 1
    page_size: int = 20
    crop_id: Optional[str] = None
    farm_id: Optional[str] = None
    field_id: Optional[str] = None
    detection_type: Optional[str] = None
    severity: Optional[str] = None
    risk_level: Optional[str] = None
    expert_verified: Optional[bool] = None
    search: Optional[str] = None
    sort_by: Optional[str] = "newest"  # newest, oldest, highest_confidence, highest_severity

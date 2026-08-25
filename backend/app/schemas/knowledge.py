from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

# --- Crop Schemas ---
class CropBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    scientific_name: Optional[str] = None
    description: Optional[str] = None
    growth_stages: List[str] = []
    common_diseases: List[str] = []
    common_pests: List[str] = []

class CropCreate(CropBase):
    pass

class CropResponse(CropBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Disease Schemas ---
class DiseaseBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    scientific_name: Optional[str] = None
    crop_id: str
    description: str
    symptoms: List[str] = []
    causes: List[str] = []
    risk_factors: List[str] = []
    severity_levels: Dict[str, str] = {}
    prevention: List[str] = []
    management: List[str] = []
    image_examples: List[str] = []

class DiseaseCreate(DiseaseBase):
    pass

class DiseaseResponse(DiseaseBase):
    id: str
    crop: Optional[CropBriefResponse] = None if "CropBriefResponse" in globals() else None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Pest Schemas ---
class PestBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    scientific_name: Optional[str] = None
    crop_id: str
    description: str
    symptoms: List[str] = []
    damage_description: Optional[str] = None
    risk_factors: List[str] = []
    prevention: List[str] = []
    management: List[str] = []
    image_examples: List[str] = []

class PestCreate(PestBase):
    pass

class PestResponse(PestBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Recommendation Schemas ---
class RecommendationBase(BaseModel):
    title: str
    description: str
    disease_id: Optional[str] = None
    pest_id: Optional[str] = None
    priority: str = "MEDIUM"
    category: str = "MANAGEMENT"
    steps: List[str] = []
    prevention: List[str] = []

class RecommendationCreate(RecommendationBase):
    pass

class RecommendationResponse(RecommendationBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StructuredRecommendation(BaseModel):
    immediate_actions: List[str] = []
    management: List[str] = []
    prevention: List[str] = []
    monitoring: List[str] = []
    expert_review_advice: str = ""
    disclaimer: str = "AI-generated recommendations provide preliminary agricultural guidance. Always consult local certified extension officers and verify chemical label regulations before application."

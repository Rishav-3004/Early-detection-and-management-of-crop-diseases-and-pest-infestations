from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

# --- Fields ---
class FieldBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    area: float = Field(..., gt=0)
    crop_id: Optional[str] = None
    variety: Optional[str] = None
    planting_date: Optional[datetime] = None
    growth_stage: Optional[str] = "Vegetative"

class FieldCreate(FieldBase):
    farm_id: str

class FieldUpdate(BaseModel):
    name: Optional[str] = None
    area: Optional[float] = None
    crop_id: Optional[str] = None
    variety: Optional[str] = None
    planting_date: Optional[datetime] = None
    growth_stage: Optional[str] = None
    health_score: Optional[float] = None

class CropBriefResponse(BaseModel):
    id: str
    name: str
    scientific_name: Optional[str] = None

    class Config:
        from_attributes = True

class FieldResponse(FieldBase):
    id: str
    farm_id: str
    health_score: float
    crop: Optional[CropBriefResponse] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Farms ---
class FarmBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    location: str = Field(..., min_length=2, max_length=255)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    area: float = Field(default=1.0, gt=0)
    soil_type: Optional[str] = "Loamy"
    irrigation_type: Optional[str] = "Drip"

class FarmCreate(FarmBase):
    pass

class FarmUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    area: Optional[float] = None
    soil_type: Optional[str] = None
    irrigation_type: Optional[str] = None

class FarmResponse(FarmBase):
    id: str
    owner_id: str
    fields: List[FieldResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

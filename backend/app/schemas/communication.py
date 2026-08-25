from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

# --- Expert Review Schemas ---
class ExpertReviewCreate(BaseModel):
    detection_id: str
    verified_label: str = Field(..., min_length=2, max_length=150)
    corrected_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    severity: str = Field(..., pattern="^(NONE|LOW|MODERATE|HIGH|CRITICAL)$")
    is_correct_prediction: bool = True
    notes: str = Field(..., min_length=5)
    recommendation: str = Field(..., min_length=5)

class ExpertReviewUpdate(BaseModel):
    verified_label: Optional[str] = None
    corrected_confidence: Optional[float] = None
    severity: Optional[str] = None
    is_correct_prediction: Optional[bool] = None
    notes: Optional[str] = None
    recommendation: Optional[str] = None
    status: Optional[str] = None

class ExpertReviewResponse(BaseModel):
    id: str
    detection_id: str
    expert_id: Optional[str] = None
    expert_name: Optional[str] = None
    verified_label: str
    corrected_confidence: Optional[float] = None
    severity: str
    is_correct_prediction: bool
    notes: str
    recommendation: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Notification Schemas ---
class NotificationResponse(BaseModel):
    id: str
    user_id: str
    type: str
    title: str
    message: str
    priority: str
    link: Optional[str] = None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- Weather Schemas ---
class WeatherCurrentResponse(BaseModel):
    temperature: float
    humidity: float
    rainfall: float
    wind_speed: float
    weather_condition: str
    recorded_at: datetime
    risk_assessment: str
    high_disease_risk_warning: bool

class WeatherForecastDay(BaseModel):
    date: str
    temp_max: float
    temp_min: float
    humidity: float
    rainfall: float
    condition: str
    disease_favorable: bool

class WeatherForecastResponse(BaseModel):
    current: WeatherCurrentResponse
    forecast: List[WeatherForecastDay] = []

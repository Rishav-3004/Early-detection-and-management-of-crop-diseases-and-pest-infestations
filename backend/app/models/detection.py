import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Boolean, JSON, Integer, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class DetectionType(str, enum.Enum):
    DISEASE = "DISEASE"
    PEST = "PEST"
    HEALTHY = "HEALTHY"
    UNKNOWN = "UNKNOWN"

class SeverityLevel(str, enum.Enum):
    NONE = "NONE"
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class RiskLevel(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class Detection(Base):
    __tablename__ = "detections"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    farm_id = Column(String(36), ForeignKey("farms.id", ondelete="SET NULL"), nullable=True, index=True)
    field_id = Column(String(36), ForeignKey("fields.id", ondelete="SET NULL"), nullable=True, index=True)
    crop_id = Column(String(36), ForeignKey("crops.id", ondelete="SET NULL"), nullable=True, index=True)
    
    image_url = Column(String(500), nullable=False)
    original_filename = Column(String(255), nullable=True)
    detection_type = Column(String(20), default=DetectionType.DISEASE.value, nullable=False, index=True)
    predicted_label = Column(String(150), nullable=False, index=True)
    scientific_name = Column(String(150), nullable=True)
    confidence = Column(Float, nullable=False)  # 0.0 - 1.0
    severity = Column(String(20), default=SeverityLevel.MODERATE.value, nullable=False, index=True)
    affected_area_percentage = Column(Float, nullable=True)  # e.g. 25.0 %
    risk_level = Column(String(20), default=RiskLevel.MEDIUM.value, nullable=False, index=True)
    risk_score = Column(Float, default=50.0, nullable=False)  # 0 - 100
    risk_reasons = Column(JSON, default=list, nullable=False)
    model_version = Column(String(50), nullable=False)
    status = Column(String(30), default="COMPLETED", nullable=False)  # PENDING, COMPLETED, FAILED, FLAGGED
    expert_verified = Column(Boolean, default=False, nullable=False, index=True)
    is_demo = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    user = relationship("User", back_populates="detections")
    farm = relationship("Farm", back_populates="detections")
    field = relationship("Field", back_populates="detections")
    crop = relationship("Crop", back_populates="detections")
    results = relationship("DetectionResult", back_populates="detection", cascade="all, delete-orphan")
    expert_review = relationship("ExpertReview", back_populates="detection", uselist=False, cascade="all, delete-orphan")


class DetectionResult(Base):
    __tablename__ = "detection_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    detection_id = Column(String(36), ForeignKey("detections.id", ondelete="CASCADE"), nullable=False, index=True)
    label = Column(String(150), nullable=False)
    confidence = Column(Float, nullable=False)
    rank = Column(Integer, nullable=False, default=1)

    detection = relationship("Detection", back_populates="results")

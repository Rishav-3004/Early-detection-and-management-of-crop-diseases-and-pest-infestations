import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class ExpertReview(Base):
    __tablename__ = "expert_reviews"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    detection_id = Column(String(36), ForeignKey("detections.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    expert_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    verified_label = Column(String(150), nullable=False)
    corrected_confidence = Column(Float, nullable=True)
    severity = Column(String(20), nullable=False)
    is_correct_prediction = Column(Boolean, default=True, nullable=False)
    notes = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=False)
    status = Column(String(30), default="RESOLVED", nullable=False)  # PENDING_REVIEW, IN_REVIEW, RESOLVED
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    detection = relationship("Detection", back_populates="expert_review")
    expert = relationship("User", back_populates="expert_reviews")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(String(50), nullable=False)  # HIGH_RISK, EXPERT_REVIEW, WEATHER_ALERT, FOLLOW_UP, SYSTEM
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    priority = Column(String(20), default="NORMAL", nullable=False)  # LOW, NORMAL, HIGH, URGENT
    link = Column(String(255), nullable=True)
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    user = relationship("User", back_populates="notifications")


class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    farm_id = Column(String(36), ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    temperature = Column(Float, nullable=False)  # Celsius
    humidity = Column(Float, nullable=False)     # %
    rainfall = Column(Float, nullable=False, default=0.0)  # mm
    wind_speed = Column(Float, nullable=False, default=0.0)  # km/h
    weather_condition = Column(String(100), nullable=False)
    recorded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    farm = relationship("Farm", back_populates="weather_records")

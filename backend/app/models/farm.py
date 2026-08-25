import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

class Farm(Base):
    __tablename__ = "farms"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    owner_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    location = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    area = Column(Float, nullable=False, default=1.0)  # in hectares / acres
    soil_type = Column(String(100), nullable=True, default="Loamy")
    irrigation_type = Column(String(100), nullable=True, default="Drip")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    owner = relationship("User", back_populates="farms")
    fields = relationship("Field", back_populates="farm", cascade="all, delete-orphan")
    detections = relationship("Detection", back_populates="farm", cascade="all, delete-orphan")
    weather_records = relationship("WeatherRecord", back_populates="farm", cascade="all, delete-orphan")


class Field(Base):
    __tablename__ = "fields"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    farm_id = Column(String(36), ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    crop_id = Column(String(36), ForeignKey("crops.id", ondelete="SET NULL"), nullable=True, index=True)
    name = Column(String(100), nullable=False)
    area = Column(Float, nullable=False, default=0.5)
    variety = Column(String(100), nullable=True)
    planting_date = Column(DateTime(timezone=True), nullable=True)
    growth_stage = Column(String(50), nullable=True, default="Vegetative")
    health_score = Column(Float, default=100.0, nullable=False)  # 0 to 100
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    farm = relationship("Farm", back_populates="fields")
    crop = relationship("Crop", back_populates="fields")
    detections = relationship("Detection", back_populates="field", cascade="all, delete-orphan")

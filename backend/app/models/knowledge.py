import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Crop(Base):
    __tablename__ = "crops"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    scientific_name = Column(String(150), nullable=True)
    description = Column(Text, nullable=True)
    growth_stages = Column(JSON, default=list, nullable=False)
    common_diseases = Column(JSON, default=list, nullable=False)
    common_pests = Column(JSON, default=list, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    fields = relationship("Field", back_populates="crop")
    diseases = relationship("Disease", back_populates="crop", cascade="all, delete-orphan")
    pests = relationship("Pest", back_populates="crop", cascade="all, delete-orphan")
    detections = relationship("Detection", back_populates="crop")


class Disease(Base):
    __tablename__ = "diseases"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    crop_id = Column(String(36), ForeignKey("crops.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(150), nullable=False, index=True)
    scientific_name = Column(String(150), nullable=True)
    description = Column(Text, nullable=False)
    symptoms = Column(JSON, default=list, nullable=False)  # list of strings
    causes = Column(JSON, default=list, nullable=False)    # list of causes/pathogens
    risk_factors = Column(JSON, default=list, nullable=False)  # temperature, humidity etc
    severity_levels = Column(JSON, default=dict, nullable=False)  # mapping of severity description
    prevention = Column(JSON, default=list, nullable=False)
    management = Column(JSON, default=list, nullable=False)
    image_examples = Column(JSON, default=list, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    crop = relationship("Crop", back_populates="diseases")
    recommendations = relationship("Recommendation", back_populates="disease", cascade="all, delete-orphan")


class Pest(Base):
    __tablename__ = "pests"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    crop_id = Column(String(36), ForeignKey("crops.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(150), nullable=False, index=True)
    scientific_name = Column(String(150), nullable=True)
    description = Column(Text, nullable=False)
    symptoms = Column(JSON, default=list, nullable=False)
    damage_description = Column(Text, nullable=True)
    risk_factors = Column(JSON, default=list, nullable=False)
    prevention = Column(JSON, default=list, nullable=False)
    management = Column(JSON, default=list, nullable=False)
    image_examples = Column(JSON, default=list, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    crop = relationship("Crop", back_populates="pests")
    recommendations = relationship("Recommendation", back_populates="pest", cascade="all, delete-orphan")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    disease_id = Column(String(36), ForeignKey("diseases.id", ondelete="CASCADE"), nullable=True, index=True)
    pest_id = Column(String(36), ForeignKey("pests.id", ondelete="CASCADE"), nullable=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String(20), default="MEDIUM", nullable=False)  # LOW, MEDIUM, HIGH, URGENT
    category = Column(String(50), default="MANAGEMENT", nullable=False)  # IMMEDIATE_ACTION, MANAGEMENT, PREVENTION, MONITORING, EXPERT_REVIEW
    steps = Column(JSON, default=list, nullable=False)
    prevention = Column(JSON, default=list, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    disease = relationship("Disease", back_populates="recommendations")
    pest = relationship("Pest", back_populates="recommendations")

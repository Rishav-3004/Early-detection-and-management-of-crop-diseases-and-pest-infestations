import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    FARMER = "FARMER"
    EXPERT = "EXPERT"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    role = Column(String(20), default=UserRole.FARMER.value, nullable=False, index=True)
    language = Column(String(10), default="en", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    farms = relationship("Farm", back_populates="owner", cascade="all, delete-orphan")
    detections = relationship("Detection", back_populates="user", cascade="all, delete-orphan")
    expert_reviews = relationship("ExpertReview", back_populates="expert")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")

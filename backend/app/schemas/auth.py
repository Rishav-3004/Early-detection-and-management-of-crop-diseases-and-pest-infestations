from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    role: str = Field(default="FARMER", pattern="^(FARMER|EXPERT|ADMIN)$")
    language: str = Field(default="en", max_length=10)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str
    name: str
    email: str
    role: str
    language: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    role: str
    language: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    language: Optional[str] = Field(None, max_length=10)
    is_active: Optional[bool] = None

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6, max_length=100)

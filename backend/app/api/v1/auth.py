from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.response import success_response
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, RefreshTokenRequest, UserResponse, UserUpdateRequest, PasswordChangeRequest
from app.services.auth_service import auth_service
from app.api.v1.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    result = await auth_service.register(db, data)
    return success_response(data=result.dict(), message="Registration successful")

@router.post("/login", response_model=dict)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await auth_service.login(db, data)
    return success_response(data=result.dict(), message="Login successful")

@router.post("/refresh", response_model=dict)
async def refresh(data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    result = await auth_service.refresh(db, data.refresh_token)
    return success_response(data=result.dict(), message="Token refreshed successfully")

@router.post("/logout", response_model=dict)
async def logout(current_user: User = Depends(get_current_user)):
    return success_response(message="Logged out successfully")

@router.get("/me", response_model=dict)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    user_data = UserResponse.from_orm(current_user)
    return success_response(data=user_data.dict())

@router.patch("/me", response_model=dict)
async def update_profile(
    data: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    updated = await auth_service.update_profile(db, current_user.id, data)
    return success_response(data=UserResponse.from_orm(updated).dict(), message="Profile updated")

@router.post("/change-password", response_model=dict)
async def change_password(
    data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await auth_service.change_password(db, current_user.id, data)
    return success_response(message="Password changed successfully")

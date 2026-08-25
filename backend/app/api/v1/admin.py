from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List, Optional
from app.core.database import get_db
from app.core.response import success_response
from app.services.admin_service import admin_service
from app.api.v1.deps import require_admin
from app.models.user import User
from app.schemas.auth import UserResponse
from app.core.exceptions import NotFoundException

router = APIRouter(prefix="/admin", tags=["Admin Studio & Analytics"])

@router.get("/analytics", response_model=dict)
async def get_analytics(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    analytics = await admin_service.get_system_analytics(db)
    return success_response(data=analytics.dict())

@router.get("/users", response_model=dict)
async def list_users(
    role: Optional[str] = Query(None),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    query = select(User).order_by(desc(User.created_at))
    if role:
        query = query.where(User.role == role.upper())
    result = await db.execute(query)
    users = list(result.scalars().all())
    data = [UserResponse.from_orm(u).dict() for u in users]
    return success_response(data=data)

@router.patch("/users/{user_id}/status", response_model=dict)
async def toggle_user_status(
    user_id: str,
    is_active: bool,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise NotFoundException("User not found")
    
    user.is_active = is_active
    await db.commit()
    await db.refresh(user)
    return success_response(data=UserResponse.from_orm(user).dict(), message="User status updated")

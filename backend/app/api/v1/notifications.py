from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.response import success_response
from app.schemas.communication import NotificationResponse
from app.services.notification_service import notification_service
from app.api.v1.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("", response_model=dict)
async def list_notifications(
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    notifs = await notification_service.get_user_notifications(db, current_user.id, limit=limit)
    data = [NotificationResponse.from_orm(n).dict() for n in notifs]
    return success_response(data=data)

@router.patch("/{notification_id}/read", response_model=dict)
async def mark_read(
    notification_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    notif = await notification_service.mark_as_read(db, current_user.id, notification_id)
    return success_response(data=NotificationResponse.from_orm(notif).dict(), message="Notification marked as read")

@router.post("/read-all", response_model=dict)
async def mark_all_read(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    count = await notification_service.mark_all_as_read(db, current_user.id)
    return success_response(data={"marked_count": count}, message=f"Marked {count} notifications as read")

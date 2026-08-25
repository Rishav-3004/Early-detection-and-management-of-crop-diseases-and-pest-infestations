from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.communication import Notification
from app.schemas.communication import NotificationResponse
from app.core.exceptions import NotFoundException

class NotificationService:
    async def get_user_notifications(self, db: AsyncSession, user_id: str, limit: int = 20) -> List[Notification]:
        query = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(desc(Notification.created_at))
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def mark_as_read(self, db: AsyncSession, user_id: str, notification_id: str) -> Notification:
        query = select(Notification).where(Notification.id == notification_id, Notification.user_id == user_id)
        result = await db.execute(query)
        notif = result.scalar_one_or_none()
        if not notif:
            raise NotFoundException("Notification not found")
        
        notif.is_read = True
        await db.commit()
        await db.refresh(notif)
        return notif

    async def mark_all_as_read(self, db: AsyncSession, user_id: str) -> int:
        query = select(Notification).where(Notification.user_id == user_id, Notification.is_read == False)
        result = await db.execute(query)
        unread = list(result.scalars().all())
        for n in unread:
            n.is_read = True
        await db.commit()
        return len(unread)

notification_service = NotificationService()

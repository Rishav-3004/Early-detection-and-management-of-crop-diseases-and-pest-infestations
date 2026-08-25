from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from app.models.detection import Detection
from app.models.communication import ExpertReview, Notification
from app.models.user import User
from app.schemas.communication import ExpertReviewCreate, ExpertReviewUpdate, ExpertReviewResponse
from app.core.exceptions import NotFoundException, ConflictException, ForbiddenException

class ExpertService:
    async def list_pending_reviews(self, db: AsyncSession) -> List[Detection]:
        # Detections without an expert review or status is pending review
        query = (
            select(Detection)
            .where(Detection.expert_verified == False)
            .options(
                selectinload(Detection.results),
                selectinload(Detection.farm),
                selectinload(Detection.field),
                selectinload(Detection.crop),
                selectinload(Detection.user),
                selectinload(Detection.expert_review)
            )
            .order_by(desc(Detection.created_at))
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def list_completed_reviews(self, db: AsyncSession, limit: int = 50) -> List[ExpertReview]:
        query = (
            select(ExpertReview)
            .options(
                selectinload(ExpertReview.detection).selectinload(Detection.user),
                selectinload(ExpertReview.detection).selectinload(Detection.crop),
                selectinload(ExpertReview.expert)
            )
            .order_by(desc(ExpertReview.created_at))
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def submit_review(self, db: AsyncSession, expert_id: str, data: ExpertReviewCreate) -> ExpertReview:
        # Check detection
        q_det = select(Detection).where(Detection.id == data.detection_id)
        r_det = await db.execute(q_det)
        det = r_det.scalar_one_or_none()
        if not det:
            raise NotFoundException("Detection record not found")

        # Check existing review
        q_rev = select(ExpertReview).where(ExpertReview.detection_id == data.detection_id)
        r_rev = await db.execute(q_rev)
        existing = r_rev.scalar_one_or_none()
        if existing:
            raise ConflictException("An expert review has already been submitted for this detection.")

        review = ExpertReview(
            detection_id=det.id,
            expert_id=expert_id,
            verified_label=data.verified_label.strip(),
            corrected_confidence=data.corrected_confidence,
            severity=data.severity,
            is_correct_prediction=data.is_correct_prediction,
            notes=data.notes.strip(),
            recommendation=data.recommendation.strip(),
            status="RESOLVED"
        )
        db.add(review)

        # Mark detection as expert-verified without altering original AI predicted_label
        det.expert_verified = True
        if not data.is_correct_prediction:
            det.status = "FLAGGED"

        # Send notification to the farmer
        q_expert = select(User).where(User.id == expert_id)
        r_expert = await db.execute(q_expert)
        expert_user = r_expert.scalar_one_or_none()
        expert_name = expert_user.name if expert_user else "Agronomist"

        notif = Notification(
            user_id=det.user_id,
            type="EXPERT_REVIEW",
            title=f"Expert Review Completed: {det.predicted_label}",
            message=f"{expert_name} has verified and provided tailored agronomic advice for your scan.",
            priority="NORMAL",
            link=f"/detections/{det.id}"
        )
        db.add(notif)

        await db.commit()
        await db.refresh(review)
        return review

expert_service = ExpertService()

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.core.response import success_response
from app.schemas.communication import ExpertReviewCreate, ExpertReviewResponse
from app.schemas.detection import DetectionResponse
from app.services.expert_service import expert_service
from app.api.v1.deps import require_expert
from app.models.user import User

router = APIRouter(prefix="/experts", tags=["Expert Reviews"])

@router.get("/cases/pending", response_model=dict)
async def list_pending_cases(
    current_user: User = Depends(require_expert),
    db: AsyncSession = Depends(get_db)
):
    cases = await expert_service.list_pending_reviews(db)
    data = []
    for c in cases:
        data.append({
            "id": c.id,
            "user_name": c.user.name if c.user else "Farmer",
            "farm_name": c.farm.name if c.farm else None,
            "field_name": c.field.name if c.field else None,
            "crop_name": c.crop.name if c.crop else None,
            "image_url": c.image_url,
            "predicted_label": c.predicted_label,
            "confidence": c.confidence,
            "severity": c.severity,
            "risk_level": c.risk_level,
            "risk_score": c.risk_score,
            "created_at": c.created_at
        })
    return success_response(data=data)

@router.get("/cases/history", response_model=dict)
async def list_case_history(
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(require_expert),
    db: AsyncSession = Depends(get_db)
):
    reviews = await expert_service.list_completed_reviews(db, limit=limit)
    data = [
        {
            "id": r.id,
            "detection_id": r.detection_id,
            "expert_name": r.expert.name if r.expert else "Agronomist",
            "verified_label": r.verified_label,
            "original_label": r.detection.predicted_label if r.detection else "N/A",
            "severity": r.severity,
            "is_correct_prediction": r.is_correct_prediction,
            "notes": r.notes,
            "recommendation": r.recommendation,
            "status": r.status,
            "created_at": r.created_at,
            "image_url": r.detection.image_url if r.detection else ""
        }
        for r in reviews
    ]
    return success_response(data=data)

@router.post("/review", response_model=dict, status_code=status.HTTP_201_CREATED)
async def submit_case_review(
    data: ExpertReviewCreate,
    current_user: User = Depends(require_expert),
    db: AsyncSession = Depends(get_db)
):
    review = await expert_service.submit_review(db, current_user.id, data)
    return success_response(
        data=ExpertReviewResponse.from_orm(review).dict(),
        message="Expert review and agronomic prescription submitted successfully"
    )

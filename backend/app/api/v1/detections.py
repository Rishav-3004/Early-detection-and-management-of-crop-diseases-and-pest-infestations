from fastapi import APIRouter, Depends, UploadFile, File, Form, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db
from app.core.response import success_response
from app.schemas.detection import DetectionFilterParams, DetectionResponse
from app.services.detection_service import detection_service
from app.api.v1.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/detections", tags=["Crop Disease & Pest Detections"])

@router.post("/scan", response_model=dict, status_code=status.HTTP_201_CREATED)
async def scan_crop(
    file: UploadFile = File(...),
    farm_id: Optional[str] = Form(None),
    field_id: Optional[str] = Form(None),
    crop_id: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    image_bytes = await file.read()
    result = await detection_service.process_scan(
        db=db,
        user_id=current_user.id,
        image_bytes=image_bytes,
        original_filename=file.filename or "leaf_scan.jpg",
        farm_id=farm_id,
        field_id=field_id,
        crop_id=crop_id
    )
    return success_response(data=result.dict(), message="Crop scan and diagnosis completed successfully")

@router.get("", response_model=dict)
async def list_detections(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    crop_id: Optional[str] = Query(None),
    farm_id: Optional[str] = Query(None),
    field_id: Optional[str] = Query(None),
    detection_type: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    risk_level: Optional[str] = Query(None),
    expert_verified: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: Optional[str] = Query("newest"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Only filter by user_id if farmer; experts & admins can view all or own
    user_filter = current_user.id if current_user.role == "FARMER" else None

    params = DetectionFilterParams(
        page=page,
        page_size=page_size,
        crop_id=crop_id,
        farm_id=farm_id,
        field_id=field_id,
        detection_type=detection_type,
        severity=severity,
        risk_level=risk_level,
        expert_verified=expert_verified,
        search=search,
        sort_by=sort_by
    )

    result = await detection_service.list_detections(db, user_filter, params)
    return success_response(data=result.dict())

@router.get("/{detection_id}", response_model=dict)
async def get_detection(
    detection_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await detection_service.get_detection_detail(db, detection_id, user_id=current_user.id)
    return success_response(data=result.dict())

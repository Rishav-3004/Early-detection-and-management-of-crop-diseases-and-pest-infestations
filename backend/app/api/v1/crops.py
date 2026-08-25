from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.core.database import get_db
from app.core.response import success_response
from app.models.knowledge import Crop, Disease, Pest
from app.schemas.knowledge import CropCreate, CropResponse
from app.api.v1.deps import get_current_user, require_admin
from app.core.exceptions import NotFoundException
from app.models.user import User

router = APIRouter(prefix="/crops", tags=["Crops Knowledge Base"])

@router.get("", response_model=dict)
async def list_crops(db: AsyncSession = Depends(get_db)):
    query = select(Crop).order_by(Crop.name.asc())
    result = await db.execute(query)
    crops = list(result.scalars().all())
    data = [CropResponse.from_orm(c).dict() for c in crops]
    return success_response(data=data)

@router.get("/{crop_id}", response_model=dict)
async def get_crop_details(crop_id: str, db: AsyncSession = Depends(get_db)):
    query = (
        select(Crop)
        .where(Crop.id == crop_id)
        .options(selectinload(Crop.diseases), selectinload(Crop.pests))
    )
    result = await db.execute(query)
    crop = result.scalar_one_or_none()
    if not crop:
        raise NotFoundException("Crop not found")
    
    return success_response(data=CropResponse.from_orm(crop).dict())

@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_crop(
    data: CropCreate,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    crop = Crop(
        name=data.name.strip(),
        scientific_name=data.scientific_name,
        description=data.description,
        growth_stages=data.growth_stages or [],
        common_diseases=data.common_diseases or [],
        common_pests=data.common_pests or []
    )
    db.add(crop)
    await db.commit()
    await db.refresh(crop)
    return success_response(data=CropResponse.from_orm(crop).dict(), message="Crop created successfully")

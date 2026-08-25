from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional, List
from app.core.database import get_db
from app.core.response import success_response
from app.models.knowledge import Pest
from app.schemas.knowledge import PestCreate, PestResponse
from app.api.v1.deps import require_admin
from app.core.exceptions import NotFoundException
from app.models.user import User

router = APIRouter(prefix="/pests", tags=["Pests Knowledge Base"])

@router.get("", response_model=dict)
async def list_pests(
    crop_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(Pest).options(selectinload(Pest.crop))
    if crop_id:
        query = query.where(Pest.crop_id == crop_id)
    query = query.order_by(Pest.name.asc())
    result = await db.execute(query)
    pests = list(result.scalars().all())
    data = [PestResponse.from_orm(p).dict() for p in pests]
    return success_response(data=data)

@router.get("/{pest_id}", response_model=dict)
async def get_pest(pest_id: str, db: AsyncSession = Depends(get_db)):
    query = (
        select(Pest)
        .where(Pest.id == pest_id)
        .options(selectinload(Pest.crop), selectinload(Pest.recommendations))
    )
    result = await db.execute(query)
    pest = result.scalar_one_or_none()
    if not pest:
        raise NotFoundException("Pest record not found")
    return success_response(data=PestResponse.from_orm(pest).dict())

@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_pest(
    data: PestCreate,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    pest = Pest(
        crop_id=data.crop_id,
        name=data.name.strip(),
        scientific_name=data.scientific_name,
        description=data.description,
        symptoms=data.symptoms or [],
        damage_description=data.damage_description,
        risk_factors=data.risk_factors or [],
        prevention=data.prevention or [],
        management=data.management or [],
        image_examples=data.image_examples or []
    )
    db.add(pest)
    await db.commit()
    await db.refresh(pest)
    return success_response(data=PestResponse.from_orm(pest).dict(), message="Pest record created")

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional, List
from app.core.database import get_db
from app.core.response import success_response
from app.models.knowledge import Disease
from app.schemas.knowledge import DiseaseCreate, DiseaseResponse
from app.api.v1.deps import require_admin
from app.core.exceptions import NotFoundException
from app.models.user import User

router = APIRouter(prefix="/diseases", tags=["Diseases Knowledge Base"])

@router.get("", response_model=dict)
async def list_diseases(
    crop_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(Disease).options(selectinload(Disease.crop))
    if crop_id:
        query = query.where(Disease.crop_id == crop_id)
    query = query.order_by(Disease.name.asc())
    result = await db.execute(query)
    diseases = list(result.scalars().all())
    data = [DiseaseResponse.from_orm(d).dict() for d in diseases]
    return success_response(data=data)

@router.get("/{disease_id}", response_model=dict)
async def get_disease(disease_id: str, db: AsyncSession = Depends(get_db)):
    query = (
        select(Disease)
        .where(Disease.id == disease_id)
        .options(selectinload(Disease.crop), selectinload(Disease.recommendations))
    )
    result = await db.execute(query)
    disease = result.scalar_one_or_none()
    if not disease:
        raise NotFoundException("Disease record not found")
    return success_response(data=DiseaseResponse.from_orm(disease).dict())

@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_disease(
    data: DiseaseCreate,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    disease = Disease(
        crop_id=data.crop_id,
        name=data.name.strip(),
        scientific_name=data.scientific_name,
        description=data.description,
        symptoms=data.symptoms or [],
        causes=data.causes or [],
        risk_factors=data.risk_factors or [],
        severity_levels=data.severity_levels or {},
        prevention=data.prevention or [],
        management=data.management or [],
        image_examples=data.image_examples or []
    )
    db.add(disease)
    await db.commit()
    await db.refresh(disease)
    return success_response(data=DiseaseResponse.from_orm(disease).dict(), message="Disease record created")

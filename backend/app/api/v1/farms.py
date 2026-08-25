from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.core.response import success_response
from app.schemas.farm import FarmCreate, FarmUpdate, FarmResponse, FieldCreate, FieldUpdate, FieldResponse
from app.services.farm_service import farm_service
from app.api.v1.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/farms", tags=["Farms"])

@router.get("", response_model=dict)
async def list_farms(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    farms = await farm_service.get_user_farms(db, current_user.id)
    data = [FarmResponse.from_orm(f).dict() for f in farms]
    return success_response(data=data)

@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_farm(
    data: FarmCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    farm = await farm_service.create_farm(db, current_user.id, data)
    return success_response(data=FarmResponse.from_orm(farm).dict(), message="Farm created successfully")

@router.get("/{farm_id}", response_model=dict)
async def get_farm(
    farm_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    farm = await farm_service.get_farm_by_id(db, farm_id, current_user.id)
    return success_response(data=FarmResponse.from_orm(farm).dict())

@router.put("/{farm_id}", response_model=dict)
async def update_farm(
    farm_id: str,
    data: FarmUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    farm = await farm_service.update_farm(db, farm_id, current_user.id, data)
    return success_response(data=FarmResponse.from_orm(farm).dict(), message="Farm updated successfully")

@router.delete("/{farm_id}", response_model=dict)
async def delete_farm(
    farm_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await farm_service.delete_farm(db, farm_id, current_user.id)
    return success_response(message="Farm deleted successfully")

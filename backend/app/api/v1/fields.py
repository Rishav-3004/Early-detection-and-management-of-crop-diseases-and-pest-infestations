from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.response import success_response
from app.schemas.farm import FieldCreate, FieldUpdate, FieldResponse
from app.services.farm_service import farm_service
from app.api.v1.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/fields", tags=["Fields"])

@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_field(
    data: FieldCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    field = await farm_service.create_field(db, current_user.id, data)
    return success_response(data=FieldResponse.from_orm(field).dict(), message="Field created successfully")

@router.get("/{field_id}", response_model=dict)
async def get_field(
    field_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    field = await farm_service.get_field_by_id(db, field_id, current_user.id)
    return success_response(data=FieldResponse.from_orm(field).dict())

@router.put("/{field_id}", response_model=dict)
async def update_field(
    field_id: str,
    data: FieldUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    field = await farm_service.update_field(db, field_id, current_user.id, data)
    return success_response(data=FieldResponse.from_orm(field).dict(), message="Field updated successfully")

@router.delete("/{field_id}", response_model=dict)
async def delete_field(
    field_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await farm_service.delete_field(db, field_id, current_user.id)
    return success_response(message="Field deleted successfully")

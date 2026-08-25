from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from sqlalchemy.orm import selectinload
from app.models.farm import Farm, Field
from app.models.knowledge import Crop
from app.models.detection import Detection
from app.schemas.farm import FarmCreate, FarmUpdate, FieldCreate, FieldUpdate
from app.core.exceptions import NotFoundException, ForbiddenException

class FarmService:
    # --- Farm Operations ---
    async def create_farm(self, db: AsyncSession, owner_id: str, data: FarmCreate) -> Farm:
        farm = Farm(
            owner_id=owner_id,
            name=data.name.strip(),
            location=data.location.strip(),
            latitude=data.latitude,
            longitude=data.longitude,
            area=data.area,
            soil_type=data.soil_type or "Loamy",
            irrigation_type=data.irrigation_type or "Drip",
        )
        db.add(farm)
        await db.commit()
        return await self.get_farm_by_id(db, farm.id)

    async def get_user_farms(self, db: AsyncSession, user_id: str) -> List[Farm]:
        query = (
            select(Farm)
            .where(Farm.owner_id == user_id)
            .options(selectinload(Farm.fields).selectinload(Field.crop))
            .order_by(Farm.created_at.desc())
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_farm_by_id(self, db: AsyncSession, farm_id: str, user_id: Optional[str] = None) -> Farm:
        query = (
            select(Farm)
            .where(Farm.id == farm_id)
            .options(selectinload(Farm.fields).selectinload(Field.crop))
        )
        result = await db.execute(query)
        farm = result.scalar_one_or_none()
        if not farm:
            raise NotFoundException("Farm not found")
        if user_id and farm.owner_id != user_id:
            raise ForbiddenException("You do not have access to this farm")
        return farm

    async def update_farm(self, db: AsyncSession, farm_id: str, user_id: str, data: FarmUpdate) -> Farm:
        farm = await self.get_farm_by_id(db, farm_id, user_id)
        if data.name is not None:
            farm.name = data.name.strip()
        if data.location is not None:
            farm.location = data.location.strip()
        if data.latitude is not None:
            farm.latitude = data.latitude
        if data.longitude is not None:
            farm.longitude = data.longitude
        if data.area is not None:
            farm.area = data.area
        if data.soil_type is not None:
            farm.soil_type = data.soil_type
        if data.irrigation_type is not None:
            farm.irrigation_type = data.irrigation_type

        await db.commit()
        return await self.get_farm_by_id(db, farm.id)

    async def delete_farm(self, db: AsyncSession, farm_id: str, user_id: str) -> bool:
        farm = await self.get_farm_by_id(db, farm_id, user_id)
        await db.delete(farm)
        await db.commit()
        return True

    # --- Field Operations ---
    async def create_field(self, db: AsyncSession, user_id: str, data: FieldCreate) -> Field:
        # Verify farm ownership
        await self.get_farm_by_id(db, data.farm_id, user_id)

        field = Field(
            farm_id=data.farm_id,
            crop_id=data.crop_id,
            name=data.name.strip(),
            area=data.area,
            variety=data.variety,
            planting_date=data.planting_date,
            growth_stage=data.growth_stage or "Vegetative",
            health_score=100.0
        )
        db.add(field)
        await db.commit()
        return await self.get_field_by_id(db, field.id)

    async def get_field_by_id(self, db: AsyncSession, field_id: str, user_id: Optional[str] = None) -> Field:
        query = (
            select(Field)
            .where(Field.id == field_id)
            .options(selectinload(Field.crop), selectinload(Field.farm))
        )
        result = await db.execute(query)
        field = result.scalar_one_or_none()
        if not field:
            raise NotFoundException("Field not found")
        if user_id and field.farm.owner_id != user_id:
            raise ForbiddenException("You do not have access to this field")
        return field

    async def update_field(self, db: AsyncSession, field_id: str, user_id: str, data: FieldUpdate) -> Field:
        field = await self.get_field_by_id(db, field_id, user_id)
        if data.name is not None:
            field.name = data.name.strip()
        if data.area is not None:
            field.area = data.area
        if data.crop_id is not None:
            field.crop_id = data.crop_id
        if data.variety is not None:
            field.variety = data.variety
        if data.planting_date is not None:
            field.planting_date = data.planting_date
        if data.growth_stage is not None:
            field.growth_stage = data.growth_stage
        if data.health_score is not None:
            field.health_score = max(0.0, min(100.0, data.health_score))

        await db.commit()
        await db.refresh(field)
        return field

    async def delete_field(self, db: AsyncSession, field_id: str, user_id: str) -> bool:
        field = await self.get_field_by_id(db, field_id, user_id)
        await db.delete(field)
        await db.commit()
        return True

    async def update_field_health(self, db: AsyncSession, field_id: str, new_detection_severity: str) -> float:
        query = select(Field).where(Field.id == field_id)
        result = await db.execute(query)
        field = result.scalar_one_or_none()
        if not field:
            return 100.0

        # Adjust score based on recent detection
        penalty = {
            "NONE": -2.0,       # Recovery
            "LOW": 4.0,
            "MODERATE": 10.0,
            "HIGH": 20.0,
            "CRITICAL": 35.0
        }.get(new_detection_severity.upper(), 5.0)

        new_health = max(10.0, min(100.0, field.health_score - penalty))
        field.health_score = round(new_health, 1)
        await db.commit()
        return field.health_score

farm_service = FarmService()

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.export_service import export_service
from app.api.v1.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/export", tags=["Data Export"])

@router.get("/csv")
async def export_csv(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    csv_content = await export_service.export_detections_csv(db, current_user.id)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=crop_disease_scans_{current_user.id[:8]}.csv"
        }
    )

import io
import csv
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from app.models.detection import Detection
from app.models.farm import Farm, Field
from app.models.knowledge import Crop

class ExportService:
    async def export_detections_csv(self, db: AsyncSession, user_id: str) -> str:
        query = (
            select(Detection)
            .where(Detection.user_id == user_id)
            .options(selectinload(Detection.farm), selectinload(Detection.field), selectinload(Detection.crop))
            .order_by(desc(Detection.created_at))
        )
        result = await db.execute(query)
        detections = list(result.scalars().all())

        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write CSV Header
        writer.writerow([
            "Detection ID",
            "Date",
            "Farm",
            "Field",
            "Crop",
            "Detection Type",
            "Diagnosis Label",
            "Scientific Name",
            "Confidence (%)",
            "Severity",
            "Risk Level",
            "Risk Score",
            "Expert Verified",
            "Status"
        ])

        for d in detections:
            writer.writerow([
                d.id,
                d.created_at.strftime("%Y-%m-%d %H:%M:%S") if d.created_at else "",
                d.farm.name if d.farm else "N/A",
                d.field.name if d.field else "N/A",
                d.crop.name if d.crop else "N/A",
                d.detection_type,
                d.predicted_label,
                d.scientific_name or "",
                round(d.confidence * 100, 1),
                d.severity,
                d.risk_level,
                d.risk_score,
                "Yes" if d.expert_verified else "No",
                d.status
            ])

        return output.getvalue()

export_service = ExportService()

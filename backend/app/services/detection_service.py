from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, asc
from sqlalchemy.orm import selectinload
from app.models.user import User
from app.models.detection import Detection, DetectionResult, DetectionType, SeverityLevel, RiskLevel
from app.models.farm import Farm, Field
from app.models.knowledge import Crop, Disease, Pest
from app.models.communication import Notification, ExpertReview
from app.schemas.detection import DetectionResponse, DetectionDetailResponse, DetectionFilterParams
from app.schemas.common import PaginatedResponse, MetaResponse
from app.schemas.knowledge import StructuredRecommendation
from app.ml.registry import model_registry
from app.storage.base import get_storage_provider
from app.weather.base import get_weather_provider
from app.services.risk_engine import risk_engine
from app.services.recommendation_engine import recommendation_engine
from app.core.exceptions import NotFoundException, ForbiddenException
from app.core.logging import logger

class DetectionService:
    async def process_scan(
        self,
        db: AsyncSession,
        user_id: str,
        image_bytes: bytes,
        original_filename: str,
        farm_id: Optional[str] = None,
        field_id: Optional[str] = None,
        crop_id: Optional[str] = None
    ) -> DetectionDetailResponse:
        # 1. Fetch Crop / Field context if supplied
        crop_name = None
        growth_stage = None
        farm_location_lat = None
        farm_location_lon = None
        farm_name = None
        field_name = None

        if field_id:
            query = select(Field).where(Field.id == field_id).options(selectinload(Field.crop), selectinload(Field.farm))
            res = await db.execute(query)
            field = res.scalar_one_or_none()
            if field:
                field_name = field.name
                growth_stage = field.growth_stage
                if not farm_id and field.farm_id:
                    farm_id = field.farm_id
                if not crop_id and field.crop_id:
                    crop_id = field.crop_id
                if field.crop:
                    crop_name = field.crop.name

        if farm_id:
            q_farm = select(Farm).where(Farm.id == farm_id)
            r_farm = await db.execute(q_farm)
            farm = r_farm.scalar_one_or_none()
            if farm:
                farm_name = farm.name
                farm_location_lat = farm.latitude
                farm_location_lon = farm.longitude

        if crop_id and not crop_name:
            q_crop = select(Crop).where(Crop.id == crop_id)
            r_crop = await db.execute(q_crop)
            crop_obj = r_crop.scalar_one_or_none()
            if crop_obj:
                crop_name = crop_obj.name

        # 2. Save Image via Storage Provider
        storage = get_storage_provider()
        image_url = await storage.save_file(image_bytes, original_filename)

        # 3. Perform ML Inference
        model = model_registry.get_model()
        diagnosis = await model.predict(image_bytes, crop_hint=crop_name, filename=original_filename)

        # 4. Fetch Weather for Environmental Context
        weather_provider = get_weather_provider()
        weather = await weather_provider.get_current_weather(
            latitude=farm_location_lat or 28.6139,
            longitude=farm_location_lon or 77.2090
        )

        # 5. Check Recent Detections on same field
        recent_count = 0
        if field_id:
            q_count = select(func.count(Detection.id)).where(
                Detection.field_id == field_id,
                Detection.detection_type != "HEALTHY"
            )
            r_count = await db.execute(q_count)
            recent_count = r_count.scalar() or 0

        # 6. Multi-Factor Risk Assessment
        risk_result = risk_engine.evaluate_risk(
            detection_type=diagnosis.detection_type,
            predicted_label=diagnosis.predicted_label,
            confidence=diagnosis.confidence,
            severity=diagnosis.severity,
            growth_stage=growth_stage,
            weather=weather,
            recent_field_detections_count=recent_count
        )

        # 7. Generate Structured Agronomic Recommendations
        recommendations = recommendation_engine.generate_recommendations(
            crop_name=crop_name,
            predicted_label=diagnosis.predicted_label,
            detection_type=diagnosis.detection_type,
            severity=diagnosis.severity,
            risk_level=risk_result.risk_level,
            risk_score=risk_result.risk_score,
            symptoms=diagnosis.symptoms
        )

        # 8. Persist Detection Record
        detection = Detection(
            user_id=user_id,
            farm_id=farm_id,
            field_id=field_id,
            crop_id=crop_id,
            image_url=image_url,
            original_filename=original_filename,
            detection_type=diagnosis.detection_type,
            predicted_label=diagnosis.predicted_label,
            scientific_name=diagnosis.scientific_name,
            confidence=diagnosis.confidence,
            severity=diagnosis.severity,
            affected_area_percentage=diagnosis.affected_area_percentage,
            risk_level=risk_result.risk_level,
            risk_score=risk_result.risk_score,
            risk_reasons=risk_result.reasons,
            model_version=diagnosis.model_version,
            status="COMPLETED",
            expert_verified=False,
            is_demo=diagnosis.is_demo
        )
        db.add(detection)
        await db.flush()

        # 9. Persist Multi-Rank Prediction Candidates
        for cand in diagnosis.candidates:
            det_res = DetectionResult(
                detection_id=detection.id,
                label=cand.label,
                confidence=cand.confidence,
                rank=cand.rank
            )
            db.add(det_res)

        # 10. Update Field Health Score if field provided
        if field_id:
            from app.services.farm_service import farm_service
            await farm_service.update_field_health(db, field_id, diagnosis.severity)

        # 11. Trigger High-Risk Alert Notification
        if risk_result.risk_level in ["HIGH", "CRITICAL"]:
            notif = Notification(
                user_id=user_id,
                type="HIGH_RISK",
                title=f"Critical Alert: {diagnosis.predicted_label}",
                message=f"High risk ({risk_result.risk_score}/100) detected on {field_name or 'crop'}. Immediate management action advised.",
                priority="HIGH",
                link=f"/detections/{detection.id}"
            )
            db.add(notif)

        await db.commit()
        await db.refresh(detection)

        return await self.get_detection_detail(db, detection.id, user_id=user_id)

    async def get_detection_detail(self, db: AsyncSession, detection_id: str, user_id: Optional[str] = None) -> DetectionDetailResponse:
        query = (
            select(Detection)
            .where(Detection.id == detection_id)
            .options(
                selectinload(Detection.results),
                selectinload(Detection.expert_review),
                selectinload(Detection.farm),
                selectinload(Detection.field),
                selectinload(Detection.crop)
            )
        )
        result = await db.execute(query)
        det = result.scalar_one_or_none()
        if not det:
            raise NotFoundException("Detection record not found")

        # Basic ownership / access check (Admins and Experts can view any case)
        # For farmers, ensure user_id matches
        if user_id:
            # Check user role if needed or simple owner check
            q_user = select(User).where(User.id == user_id)
            r_user = await db.execute(q_user)
            u = r_user.scalar_one_or_none()
            if u and u.role == "FARMER" and det.user_id != user_id:
                raise ForbiddenException("You do not have permission to view this detection")

        # Generate recommendation dynamically for detailed view
        crop_name = det.crop.name if det.crop else None
        recs = recommendation_engine.generate_recommendations(
            crop_name=crop_name,
            predicted_label=det.predicted_label,
            detection_type=det.detection_type,
            severity=det.severity,
            risk_level=det.risk_level,
            risk_score=det.risk_score,
            symptoms=[]
        )

        return DetectionDetailResponse(
            id=det.id,
            user_id=det.user_id,
            farm_id=det.farm_id,
            field_id=det.field_id,
            crop_id=det.crop_id,
            image_url=det.image_url,
            original_filename=det.original_filename,
            detection_type=det.detection_type,
            predicted_label=det.predicted_label,
            scientific_name=det.scientific_name,
            confidence=det.confidence,
            severity=det.severity,
            affected_area_percentage=det.affected_area_percentage,
            risk_level=det.risk_level,
            risk_score=det.risk_score,
            risk_reasons=det.risk_reasons or [],
            model_version=det.model_version,
            status=det.status,
            expert_verified=det.expert_verified,
            is_demo=det.is_demo,
            created_at=det.created_at,
            results=[
                {"id": r.id, "label": r.label, "confidence": r.confidence, "rank": r.rank}
                for r in sorted(det.results, key=lambda x: x.rank)
            ],
            expert_review=det.expert_review,
            symptoms=[],
            causes=[],
            recommendations=recs,
            farm_name=det.farm.name if det.farm else None,
            field_name=det.field.name if det.field else None,
            crop_name=crop_name
        )

    async def list_detections(
        self,
        db: AsyncSession,
        user_id: Optional[str],
        params: DetectionFilterParams
    ) -> PaginatedResponse[DetectionResponse]:
        query = select(Detection).options(
            selectinload(Detection.results),
            selectinload(Detection.expert_review)
        )

        # Filters
        if user_id:
            query = query.where(Detection.user_id == user_id)
        if params.crop_id:
            query = query.where(Detection.crop_id == params.crop_id)
        if params.farm_id:
            query = query.where(Detection.farm_id == params.farm_id)
        if params.field_id:
            query = query.where(Detection.field_id == params.field_id)
        if params.detection_type:
            query = query.where(Detection.detection_type == params.detection_type.upper())
        if params.severity:
            query = query.where(Detection.severity == params.severity.upper())
        if params.risk_level:
            query = query.where(Detection.risk_level == params.risk_level.upper())
        if params.expert_verified is not None:
            query = query.where(Detection.expert_verified == params.expert_verified)
        if params.search:
            search_pattern = f"%{params.search.strip()}%"
            query = query.where(Detection.predicted_label.ilike(search_pattern))

        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total_res = await db.execute(count_query)
        total = total_res.scalar() or 0

        # Sorting
        if params.sort_by == "oldest":
            query = query.order_by(asc(Detection.created_at))
        elif params.sort_by == "highest_confidence":
            query = query.order_by(desc(Detection.confidence))
        elif params.sort_by == "highest_severity":
            query = query.order_by(desc(Detection.risk_score))
        else:  # newest default
            query = query.order_by(desc(Detection.created_at))

        # Pagination
        offset = (params.page - 1) * params.page_size
        query = query.offset(offset).limit(params.page_size)

        result = await db.execute(query)
        detections = list(result.scalars().all())

        items = [
            DetectionResponse(
                id=d.id,
                user_id=d.user_id,
                farm_id=d.farm_id,
                field_id=d.field_id,
                crop_id=d.crop_id,
                image_url=d.image_url,
                original_filename=d.original_filename,
                detection_type=d.detection_type,
                predicted_label=d.predicted_label,
                scientific_name=d.scientific_name,
                confidence=d.confidence,
                severity=d.severity,
                affected_area_percentage=d.affected_area_percentage,
                risk_level=d.risk_level,
                risk_score=d.risk_score,
                risk_reasons=d.risk_reasons or [],
                model_version=d.model_version,
                status=d.status,
                expert_verified=d.expert_verified,
                is_demo=d.is_demo,
                created_at=d.created_at,
                results=[
                    {"id": r.id, "label": r.label, "confidence": r.confidence, "rank": r.rank}
                    for r in sorted(d.results, key=lambda x: x.rank)
                ],
                expert_review=d.expert_review
            )
            for d in detections
        ]

        total_pages = max(1, (total + params.page_size - 1) // params.page_size)

        return PaginatedResponse[DetectionResponse](
            items=items,
            meta=MetaResponse(
                total=total,
                page=params.page,
                page_size=params.page_size,
                total_pages=total_pages
            )
        )

detection_service = DetectionService()

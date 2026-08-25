from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, case
from datetime import datetime, timedelta, timezone
from app.models.user import User, UserRole
from app.models.farm import Farm, Field
from app.models.knowledge import Crop, Disease, Pest
from app.models.detection import Detection, DetectionType
from app.models.communication import ExpertReview
from app.schemas.admin import AdminAnalyticsResponse, SystemKPIs, ModelPerformanceMetrics, TrendDataPoint, DistributionItem

class AdminService:
    async def get_system_analytics(self, db: AsyncSession) -> AdminAnalyticsResponse:
        # 1. User & Farm Counts
        total_users = (await db.execute(select(func.count(User.id)))).scalar() or 0
        total_farmers = (await db.execute(select(func.count(User.id)).where(User.role == UserRole.FARMER.value))).scalar() or 0
        total_experts = (await db.execute(select(func.count(User.id)).where(User.role == UserRole.EXPERT.value))).scalar() or 0
        total_farms = (await db.execute(select(func.count(Farm.id)))).scalar() or 0
        total_fields = (await db.execute(select(func.count(Field.id)))).scalar() or 0

        # 2. Scans & Detection Counts
        total_scans = (await db.execute(select(func.count(Detection.id)))).scalar() or 0
        total_diseases = (await db.execute(select(func.count(Detection.id)).where(Detection.detection_type == "DISEASE"))).scalar() or 0
        total_pests = (await db.execute(select(func.count(Detection.id)).where(Detection.detection_type == "PEST"))).scalar() or 0
        total_healthy = (await db.execute(select(func.count(Detection.id)).where(Detection.detection_type == "HEALTHY"))).scalar() or 0

        # 3. Expert Reviews
        completed_reviews = (await db.execute(select(func.count(ExpertReview.id)))).scalar() or 0
        pending_reviews = max(0, total_scans - completed_reviews)

        kpis = SystemKPIs(
            total_users=total_users,
            total_farmers=total_farmers,
            total_experts=total_experts,
            total_farms=total_farms,
            total_fields=total_fields,
            total_scans=total_scans,
            total_diseases_detected=total_diseases,
            total_pests_detected=total_pests,
            total_healthy_scans=total_healthy,
            pending_expert_reviews=pending_reviews,
            completed_expert_reviews=completed_reviews
        )

        # 4. Model Metrics
        avg_conf = (await db.execute(select(func.avg(Detection.confidence)))).scalar() or 0.88
        high_conf = (await db.execute(select(func.count(Detection.id)).where(Detection.confidence >= 0.80))).scalar() or 0
        med_conf = (await db.execute(select(func.count(Detection.id)).where(Detection.confidence >= 0.60, Detection.confidence < 0.80))).scalar() or 0
        low_conf = (await db.execute(select(func.count(Detection.id)).where(Detection.confidence < 0.60))).scalar() or 0

        expert_corrections = (await db.execute(select(func.count(ExpertReview.id)).where(ExpertReview.is_correct_prediction == False))).scalar() or 0
        expert_agreement = (await db.execute(select(func.count(ExpertReview.id)).where(ExpertReview.is_correct_prediction == True))).scalar() or 0

        agreement_rate = round((expert_agreement / max(1, completed_reviews)) * 100, 1)
        correction_rate = round((expert_corrections / max(1, completed_reviews)) * 100, 1)

        model_metrics = ModelPerformanceMetrics(
            model_version="v1.2.0-agrishield",
            total_predictions=total_scans,
            average_confidence=round(avg_conf, 3),
            high_confidence_count=high_conf,
            medium_confidence_count=med_conf,
            low_confidence_count=low_conf,
            expert_verified_count=completed_reviews,
            expert_agreement_rate=agreement_rate,
            expert_correction_rate=correction_rate
        )

        # 5. Top Diseases & Pests Breakdown
        q_top_dis = (
            select(Detection.predicted_label, func.count(Detection.id).label("count"))
            .where(Detection.detection_type == "DISEASE")
            .group_by(Detection.predicted_label)
            .order_by(desc("count"))
            .limit(5)
        )
        r_top_dis = (await db.execute(q_top_dis)).all()
        top_diseases = [
            DistributionItem(
                name=r[0],
                count=r[1],
                percentage=round((r[1] / max(1, total_diseases)) * 100, 1)
            )
            for r in r_top_dis
        ]

        q_top_pests = (
            select(Detection.predicted_label, func.count(Detection.id).label("count"))
            .where(Detection.detection_type == "PEST")
            .group_by(Detection.predicted_label)
            .order_by(desc("count"))
            .limit(5)
        )
        r_top_pests = (await db.execute(q_top_pests)).all()
        top_pests = [
            DistributionItem(
                name=r[0],
                count=r[1],
                percentage=round((r[1] / max(1, total_pests)) * 100, 1)
            )
            for r in r_top_pests
        ]

        # 6. Severity Distribution
        q_sev = (
            select(Detection.severity, func.count(Detection.id).label("count"))
            .group_by(Detection.severity)
            .order_by(desc("count"))
        )
        r_sev = (await db.execute(q_sev)).all()
        sev_dist = [
            DistributionItem(
                name=r[0],
                count=r[1],
                percentage=round((r[1] / max(1, total_scans)) * 100, 1)
            )
            for r in r_sev
        ]

        # 7. 14-Day Daily Trends
        trends: List[TrendDataPoint] = []
        today = datetime.now()
        for i in range(13, -1, -1):
            day_start = (today - timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            day_str = day_start.strftime("%b %d")

            q_day = select(
                func.count(Detection.id),
                func.sum(case((Detection.detection_type == "DISEASE", 1), else_=0)),
                func.sum(case((Detection.detection_type == "PEST", 1), else_=0)),
                func.sum(case((Detection.detection_type == "HEALTHY", 1), else_=0))
            ).where(Detection.created_at >= day_start, Detection.created_at < day_end)
            
            day_res = (await db.execute(q_day)).one()
            trends.append(
                TrendDataPoint(
                    date=day_str,
                    scans=day_res[0] or 0,
                    diseases=day_res[1] or 0,
                    pests=day_res[2] or 0,
                    healthy=day_res[3] or 0
                )
            )

        return AdminAnalyticsResponse(
            kpis=kpis,
            model_metrics=model_metrics,
            daily_trends=trends,
            top_diseases=top_diseases,
            top_pests=top_pests,
            crop_distribution=[],
            severity_distribution=sev_dist
        )

admin_service = AdminService()

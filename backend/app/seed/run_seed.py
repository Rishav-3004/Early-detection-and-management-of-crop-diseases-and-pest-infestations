import asyncio
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from app.core.database import engine, Base, AsyncSessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.farm import Farm, Field
from app.models.knowledge import Crop, Disease, Pest, Recommendation
from app.models.detection import Detection, DetectionResult
from app.models.communication import ExpertReview, Notification, WeatherRecord
from app.seed.seed_data import SEED_CROPS, SEED_DISEASES, SEED_PESTS
from app.core.logging import logger

async def run_seed():
    logger.info("Initializing database schema...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        # 1. Seed Users (Farmer, Expert, Admin)
        users = [
            {
                "email": "farmer@example.com",
                "name": "Rohan Patel (Farmer)",
                "password": "Password123!",
                "role": UserRole.FARMER.value,
                "phone": "+91 98765 43210"
            },
            {
                "email": "expert@example.com",
                "name": "Dr. Sarah Jenkins (Senior Agronomist)",
                "password": "Password123!",
                "role": UserRole.EXPERT.value,
                "phone": "+1 (555) 234-5678"
            },
            {
                "email": "admin@example.com",
                "name": "System Administrator",
                "password": "Password123!",
                "role": UserRole.ADMIN.value,
                "phone": "+1 (555) 999-0000"
            }
        ]

        created_users = {}
        for u in users:
            q = select(User).where(User.email == u["email"])
            r = await db.execute(q)
            existing = r.scalar_one_or_none()
            if not existing:
                user_obj = User(
                    name=u["name"],
                    email=u["email"],
                    password_hash=get_password_hash(u["password"]),
                    role=u["role"],
                    phone=u["phone"],
                    is_active=True
                )
                db.add(user_obj)
                await db.flush()
                created_users[u["role"]] = user_obj
                logger.info(f"Seeded user: {u['email']} [{u['role']}]")
            else:
                created_users[u["role"]] = existing

        # 2. Seed Crops
        crop_map = {}
        for c in SEED_CROPS:
            q = select(Crop).where(Crop.name == c["name"])
            r = await db.execute(q)
            existing = r.scalar_one_or_none()
            if not existing:
                crop = Crop(
                    name=c["name"],
                    scientific_name=c.get("scientific_name"),
                    description=c.get("description"),
                    growth_stages=c.get("growth_stages", []),
                    common_diseases=c.get("common_diseases", []),
                    common_pests=c.get("common_pests", [])
                )
                db.add(crop)
                await db.flush()
                crop_map[c["name"]] = crop
                logger.info(f"Seeded crop: {c['name']}")
            else:
                crop_map[c["name"]] = existing

        # 3. Seed Diseases
        for d in SEED_DISEASES:
            crop_obj = crop_map.get(d["crop_name"])
            if crop_obj:
                q = select(Disease).where(Disease.name == d["name"])
                r = await db.execute(q)
                if not r.scalar_one_or_none():
                    disease = Disease(
                        crop_id=crop_obj.id,
                        name=d["name"],
                        scientific_name=d.get("scientific_name"),
                        description=d["description"],
                        symptoms=d.get("symptoms", []),
                        causes=d.get("causes", []),
                        risk_factors=d.get("risk_factors", []),
                        severity_levels=d.get("severity_levels", {}),
                        prevention=d.get("prevention", []),
                        management=d.get("management", []),
                        image_examples=[]
                    )
                    db.add(disease)
                    logger.info(f"Seeded disease: {d['name']}")

        # 4. Seed Pests
        for p in SEED_PESTS:
            crop_obj = crop_map.get(p["crop_name"])
            if crop_obj:
                q = select(Pest).where(Pest.name == p["name"])
                r = await db.execute(q)
                if not r.scalar_one_or_none():
                    pest = Pest(
                        crop_id=crop_obj.id,
                        name=p["name"],
                        scientific_name=p.get("scientific_name"),
                        description=p["description"],
                        symptoms=p.get("symptoms", []),
                        damage_description=p.get("damage_description"),
                        risk_factors=p.get("risk_factors", []),
                        prevention=p.get("prevention", []),
                        management=p.get("management", []),
                        image_examples=[]
                    )
                    db.add(pest)
                    logger.info(f"Seeded pest: {p['name']}")

        # 5. Seed Farm & Fields for Demo Farmer
        farmer = created_users.get(UserRole.FARMER.value)
        if farmer:
            q_farm = select(Farm).where(Farm.owner_id == farmer.id)
            r_farm = await db.execute(q_farm)
            farm = r_farm.scalar_one_or_none()
            if not farm:
                farm = Farm(
                    owner_id=farmer.id,
                    name="Green Valley Agro Farm",
                    location="Punjab Agri Zone, Sector 4",
                    latitude=30.7333,
                    longitude=76.7794,
                    area=12.5,
                    soil_type="Clay Loam",
                    irrigation_type="Automated Drip"
                )
                db.add(farm)
                await db.flush()
                logger.info(f"Seeded farm: {farm.name}")

                # Add fields
                tomato_crop = crop_map.get("Tomato")
                wheat_crop = crop_map.get("Wheat")
                potato_crop = crop_map.get("Potato")

                field1 = Field(
                    farm_id=farm.id,
                    crop_id=tomato_crop.id if tomato_crop else None,
                    name="North Block - Tomato Plot A",
                    area=3.5,
                    variety="Arka Rakshak",
                    growth_stage="Flowering & Fruit Set",
                    health_score=82.0
                )
                field2 = Field(
                    farm_id=farm.id,
                    crop_id=wheat_crop.id if wheat_crop else None,
                    name="East Field - Wheat Strip 1",
                    area=5.0,
                    variety="HD 2967",
                    growth_stage="Heading & Grain Filling",
                    health_score=91.0
                )
                field3 = Field(
                    farm_id=farm.id,
                    crop_id=potato_crop.id if potato_crop else None,
                    name="South Plot - Potato Tubers",
                    area=4.0,
                    variety="Kufri Jyoti",
                    growth_stage="Tuber Bulking",
                    health_score=68.5
                )
                db.add_all([field1, field2, field3])
                await db.flush()
                logger.info("Seeded 3 demo fields")

                # 6. Seed Demo Detections & History
                det1 = Detection(
                    user_id=farmer.id,
                    farm_id=farm.id,
                    field_id=field1.id,
                    crop_id=tomato_crop.id if tomato_crop else None,
                    image_url="/uploads/demo_tomato_early_blight.jpg",
                    original_filename="leaf_tomato_plot_a.jpg",
                    detection_type="DISEASE",
                    predicted_label="Tomato Early Blight",
                    scientific_name="Alternaria solani",
                    confidence=0.91,
                    severity="MODERATE",
                    affected_area_percentage=28.5,
                    risk_level="MEDIUM",
                    risk_score=58.0,
                    risk_reasons=[
                        "High diagnostic confidence (91%) for Tomato Early Blight",
                        "Crop is in a vulnerable flowering/fruit set stage",
                        "Elevated atmospheric humidity (76%) facilitates fungal spread"
                    ],
                    model_version="v1.2.0-agrishield-demo",
                    status="COMPLETED",
                    expert_verified=True,
                    is_demo=True,
                    created_at=datetime.now(timezone.utc) - timedelta(days=2)
                )
                db.add(det1)
                await db.flush()

                # Add multi-rank candidates
                r1 = DetectionResult(detection_id=det1.id, label="Tomato Early Blight", confidence=0.91, rank=1)
                r2 = DetectionResult(detection_id=det1.id, label="Tomato Septoria Leaf Spot", confidence=0.05, rank=2)
                r3 = DetectionResult(detection_id=det1.id, label="Tomato Healthy", confidence=0.04, rank=3)
                db.add_all([r1, r2, r3])

                # Seed Expert Review for det1
                expert = created_users.get(UserRole.EXPERT.value)
                if expert:
                    rev = ExpertReview(
                        detection_id=det1.id,
                        expert_id=expert.id,
                        verified_label="Tomato Early Blight",
                        corrected_confidence=0.95,
                        severity="MODERATE",
                        is_correct_prediction=True,
                        notes="Confirmed Alternaria solani symptoms. Concentric rings visible on bottom canopy leaves.",
                        recommendation="Proceed with targeted bottom-leaf defoliation. Apply copper hydroxide 50 WP per recommended regional schedule. Avoid overhead watering.",
                        status="RESOLVED",
                        created_at=datetime.now(timezone.utc) - timedelta(days=1)
                    )
                    db.add(rev)

                # Seed Notification
                notif = Notification(
                    user_id=farmer.id,
                    type="EXPERT_REVIEW",
                    title="Expert Review Completed: Tomato Early Blight",
                    message="Dr. Sarah Jenkins has reviewed your scan and provided agronomic recommendations.",
                    priority="NORMAL",
                    link=f"/detections/{det1.id}",
                    is_read=False
                )
                db.add(notif)

        await db.commit()
        logger.info("Seed execution finished successfully!")

if __name__ == "__main__":
    asyncio.run(run_seed())

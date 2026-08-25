from fastapi import APIRouter
from app.api.v1 import auth, farms, fields, crops, diseases, pests, detections, weather, notifications, experts, admin, export

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(farms.router)
api_router.include_router(fields.router)
api_router.include_router(crops.router)
api_router.include_router(diseases.router)
api_router.include_router(pests.router)
api_router.include_router(detections.router)
api_router.include_router(weather.router)
api_router.include_router(notifications.router)
api_router.include_router(experts.router)
api_router.include_router(admin.router)
api_router.include_router(export.router)

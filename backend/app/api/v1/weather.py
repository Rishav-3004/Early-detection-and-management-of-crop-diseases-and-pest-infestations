from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.core.response import success_response
from app.weather.base import get_weather_provider

router = APIRouter(prefix="/weather", tags=["Weather Integration"])

@router.get("/current", response_model=dict)
async def get_current_weather(
    latitude: Optional[float] = Query(28.6139),
    longitude: Optional[float] = Query(77.2090)
):
    provider = get_weather_provider()
    weather = await provider.get_current_weather(latitude=latitude, longitude=longitude)
    return success_response(data=weather.dict())

@router.get("/forecast", response_model=dict)
async def get_weather_forecast(
    latitude: Optional[float] = Query(28.6139),
    longitude: Optional[float] = Query(77.2090)
):
    provider = get_weather_provider()
    forecast = await provider.get_forecast(latitude=latitude, longitude=longitude)
    return success_response(data=forecast.dict())

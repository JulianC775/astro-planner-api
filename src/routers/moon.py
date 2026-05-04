from datetime import date

from fastapi import APIRouter

from src.models.moon import MoonResponse
from src.services.astronomy import moon_data

router = APIRouter()


@router.get("/moon", response_model=MoonResponse)
async def get_moon(lat: float, lon: float, date: date) -> MoonResponse:
    return moon_data(lat, lon, date)

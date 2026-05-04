from datetime import date

from fastapi import APIRouter

from src.models.sun import SunResponse
from src.services.astronomy import sun_data

router = APIRouter()


@router.get("/sun", response_model=SunResponse)
async def get_sun(lat: float, lon: float, date: date) -> SunResponse:
    return sun_data(lat, lon, date)

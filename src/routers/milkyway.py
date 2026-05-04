from datetime import date

from fastapi import APIRouter

from src.models.milkyway import MilkyWayResponse
from src.services.astronomy import milkyway_data

router = APIRouter()


@router.get("/milkyway", response_model=MilkyWayResponse)
async def get_milkyway(lat: float, lon: float, date: date) -> MilkyWayResponse:
    return milkyway_data(lat, lon, date)

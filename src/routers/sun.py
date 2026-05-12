from datetime import date as Date
from typing import Annotated

from fastapi import APIRouter, Query

from src.models.sun import SunResponse
from src.services.astronomy import sun_data

router = APIRouter(prefix="/sun", tags=["sun"])


@router.get("", response_model=SunResponse)
async def get_sun(
    lat: Annotated[float, Query(ge=-90, le=90, description="Latitude in decimal degrees")],
    lon: Annotated[float, Query(ge=-180, le=180, description="Longitude in decimal degrees")],
    date: Date,
) -> SunResponse:
    return sun_data(lat, lon, date)

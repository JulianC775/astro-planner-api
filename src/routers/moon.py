from datetime import date as Date
from typing import Annotated

from fastapi import APIRouter, Query

from src.models.moon import MoonResponse
from src.services.astronomy import moon_data

router = APIRouter(prefix="/moon", tags=["moon"])


@router.get("", response_model=MoonResponse)
async def get_moon(
    lat: Annotated[float, Query(ge=-90, le=90, description="Latitude in decimal degrees")],
    lon: Annotated[float, Query(ge=-180, le=180, description="Longitude in decimal degrees")],
    date: Date,
) -> MoonResponse:
    return moon_data(lat, lon, date)

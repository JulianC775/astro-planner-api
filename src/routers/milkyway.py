from datetime import date as Date
from typing import Annotated

from fastapi import APIRouter, Query

from src.models.milkyway import MilkyWayResponse
from src.services.milkyway_service import get_milkyway_data

router = APIRouter(prefix="/milkyway", tags=["milkyway"])


@router.get("", response_model=MilkyWayResponse)
async def get_milkyway(
    lat: Annotated[float, Query(ge=-90, le=90, description="Latitude in decimal degrees")],
    lon: Annotated[float, Query(ge=-180, le=180, description="Longitude in decimal degrees")],
    date: Date,
) -> MilkyWayResponse:
    return MilkyWayResponse(**get_milkyway_data(lat, lon, date))

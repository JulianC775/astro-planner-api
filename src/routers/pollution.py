from typing import Annotated

from fastapi import APIRouter, Query

from src.models.pollution import PollutionResponse
from src.services.pollution import get_pollution

router = APIRouter(prefix="/pollution", tags=["pollution"])


@router.get("", response_model=PollutionResponse)
async def get_pollution_endpoint(
    lat: Annotated[float, Query(ge=-90, le=90, description="Latitude in decimal degrees")],
    lon: Annotated[float, Query(ge=-180, le=180, description="Longitude in decimal degrees")],
) -> PollutionResponse:
    return await get_pollution(lat, lon)

from fastapi import APIRouter

from src.models.pollution import PollutionResponse
from src.services.pollution import get_pollution

router = APIRouter()


@router.get("/pollution", response_model=PollutionResponse)
async def get_pollution_endpoint(lat: float, lon: float) -> PollutionResponse:
    return await get_pollution(lat, lon)

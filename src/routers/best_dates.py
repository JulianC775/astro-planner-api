import asyncio
from datetime import date

from fastapi import APIRouter, Query

from src.models.best_dates import BestDatesResponse
from src.services.astronomy import best_dates

router = APIRouter()


@router.get("/best-dates", response_model=BestDatesResponse)
async def get_best_dates(
    lat: float,
    lon: float,
    days: int = Query(default=30, ge=1, le=90),
    start: date = Query(default_factory=date.today),
) -> BestDatesResponse:
    return await asyncio.to_thread(best_dates, lat, lon, start, days)

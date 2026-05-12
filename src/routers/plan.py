import asyncio
from datetime import date as Date
from typing import Annotated

from fastapi import APIRouter, Query

from src.models.milkyway import MilkyWayResponse
from src.models.moon import MoonResponse
from src.models.plan import PlanResponse
from src.models.pollution import PollutionResponse
from src.models.sun import SunResponse
from src.services.milkyway_service import get_milkyway_data
from src.services.moon_service import get_moon_data
from src.services.pollution_service import get_pollution_data
from src.services.sun_service import get_sun_data

router = APIRouter(prefix="/plan", tags=["plan"])


@router.get("", response_model=PlanResponse)
async def get_plan(
    lat: Annotated[float, Query(ge=-90, le=90, description="Latitude in decimal degrees")],
    lon: Annotated[float, Query(ge=-180, le=180, description="Longitude in decimal degrees")],
    date: Date,
) -> PlanResponse:
    moon_data, sun_data, milkyway_data, pollution_data = await asyncio.gather(
        asyncio.to_thread(get_moon_data, lat, lon, date),
        asyncio.to_thread(get_sun_data, lat, lon, date),
        asyncio.to_thread(get_milkyway_data, lat, lon, date),
        get_pollution_data(lat, lon),
    )

    moon = MoonResponse(**moon_data)
    sun = SunResponse(**sun_data)
    milkyway = MilkyWayResponse(**milkyway_data)
    pollution = PollutionResponse(**pollution_data)

    return PlanResponse(
        moon=moon,
        sun=sun,
        milkyway=milkyway,
        pollution=pollution,
        recommendation=_recommend(moon, milkyway, pollution),
    )


def _recommend(moon: MoonResponse, milkyway: MilkyWayResponse, pollution: PollutionResponse) -> str:
    issues = []

    if moon.illumination > 50:
        issues.append(f"bright moon ({moon.illumination:.0f}% illuminated)")

    if pollution.bortle_class is not None and pollution.bortle_class >= 6:
        issues.append(f"significant light pollution (Bortle {pollution.bortle_class})")

    if not milkyway.visible:
        issues.append("Milky Way core not visible tonight")

    if not issues:
        return "Good conditions for deep-sky imaging"
    return "Challenging conditions: " + ", ".join(issues)

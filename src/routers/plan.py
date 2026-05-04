import asyncio
from datetime import date, datetime, timezone

from fastapi import APIRouter

from src.models.milkyway import MilkyWayResponse
from src.models.moon import MoonResponse
from src.models.plan import PlanResponse, ShootingWindow
from src.models.pollution import PollutionResponse
from src.models.sun import SunResponse
from src.services.astronomy import milkyway_data, moon_data, sun_data
from src.services.pollution import get_pollution

router = APIRouter()


def _compute_shooting_window(
    sun: SunResponse,
    moon: MoonResponse,
    milky_way: MilkyWayResponse,
    pollution: PollutionResponse,
) -> ShootingWindow:
    """Derive the best shooting window and a quality label from combined data."""
    # Use astronomical darkness as the base window (astro twilight end → begin)
    dark_start = sun.astronomical_twilight_end
    dark_end = sun.astronomical_twilight_begin

    # If the dark window is inverted (polar summer / bad data), no window.
    if dark_start >= dark_end:
        return ShootingWindow(start=None, end=None, quality="poor")

    # Narrow by Milky Way visibility if available.
    window_start: datetime | None = dark_start
    window_end: datetime | None = dark_end

    if milky_way.visible and milky_way.visibility_start and milky_way.visibility_end:
        # Intersect with Milky Way window.
        mw_start = milky_way.visibility_start
        mw_end = milky_way.visibility_end
        intersect_start = max(dark_start, mw_start)
        intersect_end = min(dark_end, mw_end)
        if intersect_start < intersect_end:
            window_start = intersect_start
            window_end = intersect_end

    # Quality heuristic: illumination and Bortle class.
    illumination = moon.illumination  # 0–100
    bortle = pollution.bortle_class   # 1–9

    if illumination < 25 and bortle <= 4:
        quality = "excellent"
    elif illumination < 50 and bortle <= 6:
        quality = "good"
    elif illumination < 75 and bortle <= 7:
        quality = "fair"
    else:
        quality = "poor"

    return ShootingWindow(start=window_start, end=window_end, quality=quality)


@router.get("/plan", response_model=PlanResponse)
async def get_plan(lat: float, lon: float, date: date) -> PlanResponse:
    moon_result, sun_result, mw_result, pollution_result = await asyncio.gather(
        asyncio.to_thread(moon_data, lat, lon, date),
        asyncio.to_thread(sun_data, lat, lon, date),
        asyncio.to_thread(milkyway_data, lat, lon, date),
        get_pollution(lat, lon),
    )

    shooting_window = _compute_shooting_window(
        sun_result, moon_result, mw_result, pollution_result
    )

    return PlanResponse(
        moon=moon_result,
        sun=sun_result,
        milky_way=mw_result,
        pollution=pollution_result,
        shooting_window=shooting_window,
    )

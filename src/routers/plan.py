import asyncio
from datetime import date, datetime

from fastapi import APIRouter

from src.models.milkyway import MilkyWayResponse
from src.models.moon import MoonResponse
from src.models.plan import PlanResponse, ShootingWindow
from src.models.pollution import PollutionResponse
from src.models.sun import SunResponse
from src.models.weather import WeatherResponse
from src.services.apod import get_apod
from src.services.astronomy import milkyway_data, moon_data, sun_data
from src.services.pollution import get_pollution
from src.services.weather import get_weather

router = APIRouter()


def _compute_shooting_window(
    sun: SunResponse,
    moon: MoonResponse,
    milky_way: MilkyWayResponse,
    pollution: PollutionResponse,
    weather: WeatherResponse,
) -> ShootingWindow:
    # astronomical_twilight_begin = dusk, end = dawn
    dark_start = sun.astronomical_twilight_begin
    dark_end = sun.astronomical_twilight_end

    if dark_end <= dark_start:
        return ShootingWindow(start=None, end=None, quality="poor", go=False)

    window_start: datetime | None = dark_start
    window_end: datetime | None = dark_end

    if milky_way.visible and milky_way.visibility_start and milky_way.visibility_end:
        intersect_start = max(dark_start, milky_way.visibility_start)
        intersect_end = min(dark_end, milky_way.visibility_end)
        if intersect_start < intersect_end:
            window_start = intersect_start
            window_end = intersect_end

    illumination = moon.illumination       # 0–100
    bortle = pollution.bortle_class        # 1–9
    cloud_pct = weather.cloud_cover_pct   # 0–100, -1 = unknown
    seeing = weather.seeing

    # Clouds are the hardest gate — no point shooting through thick overcast.
    if cloud_pct > 70:
        return ShootingWindow(start=window_start, end=window_end, quality="poor", go=False)

    if illumination < 25 and bortle <= 4 and cloud_pct <= 20 and seeing == "excellent":
        quality = "excellent"
    elif illumination < 50 and bortle <= 6 and cloud_pct <= 40:
        quality = "good"
    elif illumination < 75 and bortle <= 7 and cloud_pct <= 60:
        quality = "fair"
    else:
        quality = "poor"

    go = quality in ("excellent", "good")
    return ShootingWindow(start=window_start, end=window_end, quality=quality, go=go)


@router.get("/plan", response_model=PlanResponse)
async def get_plan(lat: float, lon: float, date: date) -> PlanResponse:
    moon_result, sun_result, mw_result, pollution_result, weather_result, apod_result = (
        await asyncio.gather(
            asyncio.to_thread(moon_data, lat, lon, date),
            asyncio.to_thread(sun_data, lat, lon, date),
            asyncio.to_thread(milkyway_data, lat, lon, date),
            get_pollution(lat, lon),
            get_weather(lat, lon),
            get_apod(date),
        )
    )

    shooting_window = _compute_shooting_window(
        sun_result, moon_result, mw_result, pollution_result, weather_result
    )

    return PlanResponse(
        moon=moon_result,
        sun=sun_result,
        milky_way=mw_result,
        pollution=pollution_result,
        weather=weather_result,
        apod=apod_result,
        shooting_window=shooting_window,
    )

import httpx

from src.models.weather import WeatherResponse

# 7Timer ASTRO product — purpose-built for astronomers, no API key required.
# Returns seeing, transparency, cloud cover, and wind for the next 8 days.
_7TIMER_URL = (
    "https://www.7timer.info/bin/api.pl"
    "?lon={lon}&lat={lat}&product=astro&output=json"
)

_SEEING_LABELS = {1: "excellent", 2: "good", 3: "fair", 4: "poor", 5: "poor"}
_TRANSPARENCY_LABELS = {1: "excellent", 2: "good", 3: "fair", 4: "poor", 5: "poor", 6: "poor", 7: "poor"}


def _seeing_label(val: int) -> str:
    return _SEEING_LABELS.get(val, "fair")


def _transparency_label(val: int) -> str:
    return _TRANSPARENCY_LABELS.get(val, "fair")


def _cloud_description(cloud_pct: int, seeing: str) -> str:
    if cloud_pct <= 10:
        return f"Clear skies — {seeing} seeing"
    if cloud_pct <= 40:
        return f"Mostly clear — {seeing} seeing"
    if cloud_pct <= 70:
        return "Partly cloudy"
    return "Overcast"


async def get_weather(lat: float, lon: float, target_hour_utc: int = 22) -> WeatherResponse:
    """Fetch astronomical weather from 7Timer for the given location.

    target_hour_utc: which hour of the night to pull (default 22:00 UTC).
    7Timer returns forecasts in 3-hour steps starting from the nearest
    synoptic time; we pick the step closest to the requested hour.
    """
    url = _7TIMER_URL.format(lat=lat, lon=lon)
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()

        dataseries = data.get("dataseries", [])
        if not dataseries:
            raise ValueError("empty dataseries")

        # Pick the entry whose timepoint (hours from init) is closest to target.
        # Init time from 7Timer is always 00:00 UTC of the current day.
        best = min(dataseries, key=lambda d: abs(d["timepoint"] - target_hour_utc))

        cloud_pct = int(best.get("cloudcover", 5)) * 12  # 1–9 scale → ~%
        cloud_pct = min(cloud_pct, 100)
        seeing = _seeing_label(best.get("seeing", 3))
        transparency = _transparency_label(best.get("transparency", 3))
        wind_speed = float(best.get("wind10m", {}).get("speed", 0)) * 0.5  # scale to m/s approx

        return WeatherResponse(
            cloud_cover_pct=cloud_pct,
            seeing=seeing,
            transparency=transparency,
            wind_speed_ms=round(wind_speed, 1),
            description=_cloud_description(cloud_pct, seeing),
        )

    except Exception:
        return WeatherResponse(
            cloud_cover_pct=-1,
            seeing="unknown",
            transparency="unknown",
            wind_speed_ms=-1.0,
            description="Weather data unavailable",
        )

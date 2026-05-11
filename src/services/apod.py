from datetime import date

import httpx

from src.core.config import settings
from src.models.apod import ApodResponse

_APOD_URL = "https://api.nasa.gov/planetary/apod"


async def get_apod(d: date) -> ApodResponse | None:
    """Fetch NASA Astronomy Picture of the Day for the given date.

    Returns None if APOD_API_KEY is not configured or the request fails.
    Uses DEMO_KEY if no key is set — limited to 30 requests/hour/IP.
    """
    api_key = settings.apod_api_key or "DEMO_KEY"
    params = {"api_key": api_key, "date": d.isoformat()}

    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.get(_APOD_URL, params=params)
            resp.raise_for_status()
            data = resp.json()

        return ApodResponse(
            date=data["date"],
            title=data["title"],
            explanation=data["explanation"],
            url=data["url"],
            media_type=data.get("media_type", "image"),
            hdurl=data.get("hdurl"),
        )
    except Exception:
        return None

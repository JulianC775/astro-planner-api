import math

import httpx

from src.models.pollution import PollutionResponse

# Light pollution tile service (no API key required).
# Uses the SQM (sky quality) tile layer from lightpollutionmap.info (ISSA data).
# Tile zoom level 8 gives ~600m resolution, good enough for location planning.
_TILE_URL = "https://www.lightpollutionmap.info/QueryRaster/?ql=wa_2015&qt=point&qd={lon},{lat}"

_BORTLE_DESCRIPTIONS = {
    1: "Excellent dark sky",
    2: "Truly dark sky",
    3: "Rural sky",
    4: "Rural/suburban transition",
    5: "Suburban sky",
    6: "Bright suburban sky",
    7: "Suburban/urban transition",
    8: "City sky",
    9: "Inner-city sky",
}


def _sqm_to_bortle(sqm: float) -> int:
    """Convert sky quality (mag/arcsec²) to Bortle class (1–9)."""
    if sqm >= 21.99:
        return 1
    if sqm >= 21.89:
        return 2
    if sqm >= 21.69:
        return 3
    if sqm >= 20.49:
        return 4
    if sqm >= 19.50:
        return 5
    if sqm >= 18.94:
        return 6
    if sqm >= 18.38:
        return 7
    if sqm >= 17.80:
        return 8
    return 9


def _radiance_to_sqm(radiance: float) -> float:
    """Convert artificial sky radiance (μcd/m²) to SQM (mag/arcsec²).

    Formula from Cinzano (2000): SQM ≈ -2.5 * log10(radiance / 108) + offset
    Simplified empirical conversion used widely in light pollution mapping.
    """
    if radiance <= 0:
        return 22.0
    return round(-2.5 * math.log10(radiance / 108.0) + 7.93, 2)


async def get_pollution(lat: float, lon: float) -> PollutionResponse:
    url = _TILE_URL.format(lat=lat, lon=lon)
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            # Response: {"b": <radiance_value>} where b is artificial brightness
            radiance = float(data.get("b", 0) or 0)
            sqm = _radiance_to_sqm(radiance)
            bortle = _sqm_to_bortle(sqm)
            return PollutionResponse(
                bortle_class=bortle,
                sqm=sqm,
                description=_BORTLE_DESCRIPTIONS[bortle],
            )
    except Exception:
        # Fall back to unknown rather than crashing the request.
        return PollutionResponse(
            bortle_class=5,
            sqm=None,
            description="Data unavailable — suburban sky assumed",
        )

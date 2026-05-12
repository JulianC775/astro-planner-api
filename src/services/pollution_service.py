import json
import math

import httpx

from src.core.config import settings

_BORTLE_DESCRIPTIONS = {
    1: "Excellent dark-sky site",
    2: "Truly dark site",
    3: "Rural sky",
    4: "Rural/suburban transition",
    5: "Suburban sky",
    6: "Bright suburban sky",
    7: "Suburban/urban transition",
    8: "City sky",
    9: "Inner-city sky",
}

# Natural sky background radiance used in SQM conversion (mcd/m²)
_NATURAL_RADIANCE = 0.171168


async def get_pollution_data(lat: float, lon: float) -> dict:
    try:
        radiance = await _fetch_radiance(lat, lon)
        bortle = _radiance_to_bortle(radiance)
        sqm = _radiance_to_sqm(radiance)
        return {
            "bortle_class": bortle,
            "sqm": round(sqm, 2),
            "description": _BORTLE_DESCRIPTIONS[bortle],
        }
    except Exception:
        return {
            "bortle_class": None,
            "sqm": None,
            "description": "Light pollution data unavailable",
        }


async def _fetch_radiance(lat: float, lon: float) -> float:
    qd = json.dumps({"type": "Point", "coordinates": [lon, lat]})
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            settings.pollution_api_url,
            params={"ql": "wa_2015", "qt": "point", "qd": qd},
        )
        response.raise_for_status()
        return float(response.json()["result"])


def _radiance_to_bortle(radiance: float) -> int:
    # Approximate mapping from artificial sky brightness (mcd/m²) to Bortle class
    if radiance < 0.01:
        return 1
    elif radiance < 0.08:
        return 2
    elif radiance < 0.25:
        return 3
    elif radiance < 1.0:
        return 4
    elif radiance < 3.0:
        return 5
    elif radiance < 15.0:
        return 6
    elif radiance < 50.0:
        return 7
    elif radiance < 150.0:
        return 8
    else:
        return 9


def _radiance_to_sqm(radiance: float) -> float:
    return 21.58 - 2.5 * math.log10(1 + radiance / _NATURAL_RADIANCE)

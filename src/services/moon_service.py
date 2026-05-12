import math
from datetime import date, timezone

import ephem


def get_moon_data(lat: float, lon: float, target_date: date) -> dict:
    obs = _make_observer(lat, lon, target_date)
    moon = ephem.Moon()
    moon.compute(obs)

    return {
        "phase": _compute_phase_name(obs),
        "illumination": round(float(moon.phase), 1),
        "moonrise": _safe_next_rising(obs, moon),
        "moonset": _safe_next_setting(obs, moon),
    }


def _make_observer(lat: float, lon: float, target_date: date) -> ephem.Observer:
    obs = ephem.Observer()
    obs.lat = str(lat)
    obs.lon = str(lon)
    obs.elevation = 0
    obs.pressure = 0
    obs.date = target_date.strftime("%Y/%m/%d 00:00:00")
    return obs


def _compute_phase_name(obs: ephem.Observer) -> str:
    moon = ephem.Moon(obs)
    sun = ephem.Sun(obs)
    moon_ecl = ephem.Ecliptic(moon)
    sun_ecl = ephem.Ecliptic(sun)

    phase_deg = math.degrees(
        (float(moon_ecl.lon) - float(sun_ecl.lon)) % (2 * math.pi)
    )

    if phase_deg < 22.5 or phase_deg >= 337.5:
        return "New Moon"
    elif phase_deg < 67.5:
        return "Waxing Crescent"
    elif phase_deg < 112.5:
        return "First Quarter"
    elif phase_deg < 157.5:
        return "Waxing Gibbous"
    elif phase_deg < 202.5:
        return "Full Moon"
    elif phase_deg < 247.5:
        return "Waning Gibbous"
    elif phase_deg < 292.5:
        return "Last Quarter"
    else:
        return "Waning Crescent"


def _safe_next_rising(obs: ephem.Observer, body: ephem.Body) -> str | None:
    try:
        return obs.next_rising(body).datetime().replace(tzinfo=timezone.utc).isoformat()
    except (ephem.NeverUpError, ephem.AlwaysUpError):
        return None


def _safe_next_setting(obs: ephem.Observer, body: ephem.Body) -> str | None:
    try:
        return obs.next_setting(body).datetime().replace(tzinfo=timezone.utc).isoformat()
    except (ephem.NeverUpError, ephem.AlwaysUpError):
        return None

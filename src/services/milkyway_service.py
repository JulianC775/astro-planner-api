import math
from datetime import date, datetime, timedelta, timezone

import ephem

_MIN_ALTITUDE_DEG = 5.0

# Sagittarius A* — galactic core
_GALCORE_RA = "17:45:40.04"
_GALCORE_DEC = "-29:00:28.1"


def get_milkyway_data(lat: float, lon: float, target_date: date) -> dict:
    dark_start, dark_end = _get_dark_window(lat, lon, target_date)

    if dark_start is None or dark_end is None:
        return {"visible": False, "windows": [], "galactic_core_max_altitude": 0.0}

    windows, max_alt = _compute_core_windows(lat, lon, dark_start, dark_end)

    return {
        "visible": len(windows) > 0,
        "windows": windows,
        "galactic_core_max_altitude": round(max_alt, 1),
    }


def _get_dark_window(
    lat: float, lon: float, target_date: date
) -> tuple[datetime | None, datetime | None]:
    obs = ephem.Observer()
    obs.lat = str(lat)
    obs.lon = str(lon)
    obs.elevation = 0
    obs.pressure = 0
    obs.horizon = "-18"
    obs.date = target_date.strftime("%Y/%m/%d 12:00:00")  # start from noon to find tonight's dusk

    sun = ephem.Sun()
    try:
        dusk_ephem = obs.next_setting(sun, use_center=True)
        dusk = dusk_ephem.datetime().replace(tzinfo=timezone.utc)
        obs.date = dusk_ephem
        dawn = obs.next_rising(sun, use_center=True).datetime().replace(tzinfo=timezone.utc)
        return dusk, dawn
    except (ephem.NeverUpError, ephem.AlwaysUpError):
        return None, None


def _compute_core_windows(
    lat: float, lon: float, dark_start: datetime, dark_end: datetime
) -> tuple[list[dict], float]:
    galcore = ephem.FixedBody()
    galcore._ra = _GALCORE_RA
    galcore._dec = _GALCORE_DEC
    galcore._epoch = ephem.J2000

    obs = ephem.Observer()
    obs.lat = str(lat)
    obs.lon = str(lon)
    obs.elevation = 0
    obs.pressure = 0

    windows: list[dict] = []
    window_start: datetime | None = None
    window_peak = 0.0
    max_alt = 0.0

    current = dark_start
    step = timedelta(minutes=15)

    while current <= dark_end:
        obs.date = ephem.Date(current.replace(tzinfo=None))
        galcore.compute(obs)
        alt = math.degrees(float(galcore.alt))
        max_alt = max(max_alt, alt)

        if alt >= _MIN_ALTITUDE_DEG:
            if window_start is None:
                window_start = current
            window_peak = max(window_peak, alt)
        else:
            if window_start is not None:
                windows.append(
                    {
                        "start": window_start.isoformat(),
                        "end": current.isoformat(),
                        "peak_altitude": round(window_peak, 1),
                    }
                )
                window_start = None
                window_peak = 0.0

        current += step

    if window_start is not None:
        windows.append(
            {
                "start": window_start.isoformat(),
                "end": dark_end.isoformat(),
                "peak_altitude": round(window_peak, 1),
            }
        )

    return windows, max_alt

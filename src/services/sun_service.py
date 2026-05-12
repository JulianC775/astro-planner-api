from datetime import date, timezone

import ephem


def get_sun_data(lat: float, lon: float, target_date: date) -> dict:
    sun = ephem.Sun()

    def obs(horizon: str) -> ephem.Observer:
        o = ephem.Observer()
        o.lat = str(lat)
        o.lon = str(lon)
        o.elevation = 0
        o.pressure = 0
        o.horizon = horizon
        o.date = target_date.strftime("%Y/%m/%d 00:00:00")
        return o

    return {
        "sunrise": _safe_rising(obs("-0:34"), sun),
        "sunset": _safe_setting(obs("-0:34"), sun),
        "civil_dawn": _safe_rising(obs("-6"), sun, center=True),
        "civil_dusk": _safe_setting(obs("-6"), sun, center=True),
        "nautical_dawn": _safe_rising(obs("-12"), sun, center=True),
        "nautical_dusk": _safe_setting(obs("-12"), sun, center=True),
        "astronomical_dawn": _safe_rising(obs("-18"), sun, center=True),
        "astronomical_dusk": _safe_setting(obs("-18"), sun, center=True),
    }


def _safe_rising(o: ephem.Observer, body: ephem.Body, center: bool = False) -> str | None:
    try:
        return o.next_rising(body, use_center=center).datetime().replace(tzinfo=timezone.utc).isoformat()
    except (ephem.NeverUpError, ephem.AlwaysUpError):
        return None


def _safe_setting(o: ephem.Observer, body: ephem.Body, center: bool = False) -> str | None:
    try:
        return o.next_setting(body, use_center=center).datetime().replace(tzinfo=timezone.utc).isoformat()
    except (ephem.NeverUpError, ephem.AlwaysUpError):
        return None

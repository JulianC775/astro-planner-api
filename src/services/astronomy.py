"""Astronomical calculation service using ephem.

All returned datetimes are UTC with tzinfo=timezone.utc.
"""

from datetime import date, datetime, timedelta, timezone

import ephem

from src.models.milkyway import MilkyWayResponse
from src.models.moon import MoonResponse
from src.models.sun import SunResponse

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_PHASE_NAMES = [
    (0.0, 0.02, "New Moon"),
    (0.02, 0.24, "Waxing Crescent"),
    (0.24, 0.26, "First Quarter"),
    (0.26, 0.49, "Waxing Gibbous"),
    (0.49, 0.51, "Full Moon"),
    (0.51, 0.74, "Waning Gibbous"),
    (0.74, 0.76, "Third Quarter"),
    (0.76, 0.98, "Waning Crescent"),
    (0.98, 1.01, "New Moon"),
]


def _phase_name(phase_fraction: float) -> str:
    """Return a phase name from a 0–1 moon phase fraction."""
    for lo, hi, name in _PHASE_NAMES:
        if lo <= phase_fraction < hi:
            return name
    return "New Moon"


def _ephem_date_to_utc(ephem_date: ephem.Date) -> datetime:  # type: ignore[name-defined]
    """Convert an ephem.Date to a timezone-aware UTC datetime."""
    dt = ephem_date.datetime()
    return dt.replace(tzinfo=timezone.utc)


def _make_observer(lat: float, lon: float, dt: datetime) -> ephem.Observer:  # type: ignore[name-defined]
    """Build an ephem.Observer for the given coordinates and UTC moment."""
    obs = ephem.Observer()
    obs.lat = str(lat)
    obs.lon = str(lon)
    obs.date = ephem.Date(dt.strftime("%Y/%m/%d %H:%M:%S"))
    obs.pressure = 0  # disable atmospheric refraction for consistency
    return obs


def _noon_utc(d: date) -> datetime:
    """Return noon UTC on the given date."""
    return datetime(d.year, d.month, d.day, 12, 0, 0, tzinfo=timezone.utc)


def _try_rising(obs: ephem.Observer, body: ephem.Body, use_center: bool = False) -> datetime | None:  # type: ignore[name-defined]
    try:
        return _ephem_date_to_utc(obs.next_rising(body, use_center=use_center))
    except (ephem.CircumpolarError, ephem.NeverUpError, ephem.AlwaysUpError):
        return None


def _try_setting(obs: ephem.Observer, body: ephem.Body, use_center: bool = False) -> datetime | None:  # type: ignore[name-defined]
    try:
        return _ephem_date_to_utc(obs.next_setting(body, use_center=use_center))
    except (ephem.CircumpolarError, ephem.NeverUpError, ephem.AlwaysUpError):
        return None


# ---------------------------------------------------------------------------
# Moon
# ---------------------------------------------------------------------------


def moon_data(lat: float, lon: float, d: date) -> MoonResponse:
    """Calculate moon phase and rise/set times for a given location and date."""
    noon = _noon_utc(d)
    obs = _make_observer(lat, lon, noon)

    moon = ephem.Moon()
    moon.compute(obs)

    # ephem moon_phase is the illuminated fraction (0–1).
    illumination = float(moon.moon_phase) * 100.0

    # Phase fraction based on the age in the synodic cycle.
    # ephem.Moon().phase gives illumination; we derive the cycle position
    # from the previous new moon.
    prev_new = ephem.previous_new_moon(obs.date)
    synodic_month = 29.530588853  # days
    age = float(obs.date - prev_new)
    phase_fraction = age / synodic_month

    rise = _try_rising(obs, moon)
    setting = _try_setting(obs, moon)

    return MoonResponse(
        phase_name=_phase_name(phase_fraction),
        illumination=round(illumination, 2),
        rise=rise,
        set=setting,
    )


# ---------------------------------------------------------------------------
# Sun / Twilight
# ---------------------------------------------------------------------------


def _twilight_times(
    lat: float,
    lon: float,
    noon: datetime,
    horizon: str,
) -> tuple[datetime | None, datetime | None]:
    """Return (begin, end) for a twilight type defined by the horizon string.

    For morning twilight *begin* is the rising at that horizon (sun goes up
    past it) and *end* is the corresponding setting the evening before, but
    since we want the evening *end* we use next_setting from midnight.
    """
    # Use midnight at the start of the day to search forward.
    midnight = datetime(noon.year, noon.month, noon.day, 0, 0, 0, tzinfo=timezone.utc)

    obs_morning = _make_observer(lat, lon, midnight)
    obs_morning.horizon = horizon

    obs_evening = _make_observer(lat, lon, noon)
    obs_evening.horizon = horizon

    sun = ephem.Sun()

    try:
        begin = _ephem_date_to_utc(obs_morning.next_rising(sun, use_center=False))
    except (ephem.CircumpolarError, ephem.NeverUpError, ephem.AlwaysUpError):
        begin = None

    try:
        end = _ephem_date_to_utc(obs_evening.next_setting(sun, use_center=False))
    except (ephem.CircumpolarError, ephem.NeverUpError, ephem.AlwaysUpError):
        end = None

    return begin, end


def sun_data(lat: float, lon: float, d: date) -> SunResponse:
    """Calculate sunrise, sunset, and all twilight times for a location and date."""
    noon = _noon_utc(d)
    midnight = datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=timezone.utc)

    # Standard rise/set (horizon = 0, with atmospheric refraction suppressed
    # we use the default -0°34' which ephem applies when pressure != 0;
    # here pressure=0 so we set horizon to "-0:34" to match convention).
    obs_rise = _make_observer(lat, lon, midnight)
    obs_rise.horizon = "-0:34"
    obs_set = _make_observer(lat, lon, noon)
    obs_set.horizon = "-0:34"

    sun = ephem.Sun()

    def _rising(obs: ephem.Observer) -> datetime | None:
        try:
            return _ephem_date_to_utc(obs.next_rising(sun, use_center=False))
        except (ephem.CircumpolarError, ephem.NeverUpError, ephem.AlwaysUpError):
            return None

    def _setting(obs: ephem.Observer) -> datetime | None:
        try:
            return _ephem_date_to_utc(obs.next_setting(sun, use_center=False))
        except (ephem.CircumpolarError, ephem.NeverUpError, ephem.AlwaysUpError):
            return None

    sunrise = _rising(obs_rise)
    sunset = _setting(obs_set)

    civil_begin, civil_end = _twilight_times(lat, lon, noon, "-6")
    nautical_begin, nautical_end = _twilight_times(lat, lon, noon, "-12")
    astro_begin, astro_end = _twilight_times(lat, lon, noon, "-18")

    # Provide fallback sentinels so the response model is always valid.
    _fallback = datetime(d.year, d.month, d.day, 12, 0, 0, tzinfo=timezone.utc)

    return SunResponse(
        sunrise=sunrise or _fallback,
        sunset=sunset or _fallback,
        civil_twilight_begin=civil_begin or _fallback,
        civil_twilight_end=civil_end or _fallback,
        nautical_twilight_begin=nautical_begin or _fallback,
        nautical_twilight_end=nautical_end or _fallback,
        astronomical_twilight_begin=astro_begin or _fallback,
        astronomical_twilight_end=astro_end or _fallback,
    )


# ---------------------------------------------------------------------------
# Milky Way
# ---------------------------------------------------------------------------

# Galactic centre (J2000): RA 17h 45m 40.04s, Dec -29° 00' 28.1"
_GC_RA = "17:45:40.04"
_GC_DEC = "-29:00:28.1"


def milkyway_data(lat: float, lon: float, d: date) -> MilkyWayResponse:
    """Estimate Milky Way / galactic core visibility for a location and date.

    Strategy:
    - The galactic core is modelled as a fixed star at the J2000 position.
    - We sample every 15 minutes throughout the night (astro-dark window,
      approximated as 1 hour after sunset to 1 hour before sunrise).
    - Visibility requires the core to be above the horizon (altitude > 0°).
    - We report the first and last times it is above the horizon within the
      window, and the peak altitude reached.
    """
    noon = _noon_utc(d)
    next_day_noon = noon + timedelta(days=1)

    # Approximate night window: from 20:00 to 06:00 UTC (generous; works for
    # mid-latitudes). We sample the full 24-hour day to handle all latitudes.
    sample_start = datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=timezone.utc)

    galactic_center = ephem.FixedBody()
    galactic_center._ra = _GC_RA  # type: ignore[attr-defined]
    galactic_center._dec = _GC_DEC  # type: ignore[attr-defined]
    galactic_center._epoch = ephem.J2000  # type: ignore[attr-defined]

    altitudes: list[tuple[datetime, float]] = []
    t = sample_start
    step = timedelta(minutes=15)
    while t < sample_start + timedelta(days=1):
        obs = _make_observer(lat, lon, t)
        galactic_center.compute(obs)
        alt_deg = float(galactic_center.alt) * 180.0 / 3.141592653589793
        altitudes.append((t, alt_deg))
        t += step

    above = [(dt, alt) for dt, alt in altitudes if alt > 0.0]

    if not above:
        return MilkyWayResponse(
            visible=False,
            visibility_start=None,
            visibility_end=None,
            peak_altitude=None,
        )

    visibility_start = above[0][0]
    visibility_end = above[-1][0]
    peak_altitude = round(max(alt for _, alt in above), 2)

    return MilkyWayResponse(
        visible=True,
        visibility_start=visibility_start,
        visibility_end=visibility_end,
        peak_altitude=peak_altitude,
    )

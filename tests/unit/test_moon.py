"""Unit tests for moon_data() using ephem directly."""

from datetime import date, datetime, timezone

import ephem
import pytest

from src.models.moon import MoonResponse
from src.services.astronomy import moon_data


def test_moon_data_returns_correct_types() -> None:
    """moon_data() should return a MoonResponse with correct field types."""
    result = moon_data(lat=40.7128, lon=-74.0060, d=date(2024, 6, 21))

    assert isinstance(result, MoonResponse)
    assert isinstance(result.phase_name, str)
    assert isinstance(result.illumination, float)
    # rise and set can be None (polar situations) but if present must be UTC datetimes
    if result.rise is not None:
        assert isinstance(result.rise, datetime)
        assert result.rise.tzinfo == timezone.utc
    if result.set is not None:
        assert isinstance(result.set, datetime)
        assert result.set.tzinfo == timezone.utc


def test_moon_illumination_in_valid_range() -> None:
    """Illumination should always be in the range 0–100."""
    # Test a spread of dates to cover different moon phases.
    test_dates = [
        date(2024, 1, 11),  # near new moon
        date(2024, 1, 18),  # near first quarter
        date(2024, 1, 25),  # near full moon
        date(2024, 2, 2),   # near last quarter
        date(2024, 6, 21),  # summer solstice (arbitrary)
        date(2024, 12, 15), # winter
    ]
    for d in test_dates:
        result = moon_data(lat=34.0522, lon=-118.2437, d=d)
        assert 0.0 <= result.illumination <= 100.0, (
            f"illumination {result.illumination} out of range for {d}"
        )

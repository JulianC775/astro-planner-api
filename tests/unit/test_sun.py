from datetime import date, timezone

from src.services.astronomy import _dark_hours, sun_data


def test_sun_data_returns_correct_types():
    result = sun_data(34.18, -118.31, date(2026, 1, 15))
    assert result.sunrise.tzinfo == timezone.utc
    assert result.sunset.tzinfo == timezone.utc
    assert result.astronomical_twilight_begin.tzinfo == timezone.utc
    assert result.astronomical_twilight_end.tzinfo == timezone.utc


def test_twilight_ordering():
    # For a normal mid-latitude night: sunrise < sunset, dusk < dawn
    result = sun_data(34.18, -118.31, date(2026, 1, 15))
    assert result.astronomical_twilight_begin < result.astronomical_twilight_end
    assert result.nautical_twilight_begin < result.nautical_twilight_end
    assert result.civil_twilight_begin < result.civil_twilight_end


def test_dark_hours_positive_and_plausible():
    result = sun_data(34.18, -118.31, date(2026, 1, 15))
    hours = _dark_hours(result)
    assert 6.0 <= hours <= 14.0  # winter night at 34° lat


def test_dark_hours_shorter_in_summer():
    winter = sun_data(34.18, -118.31, date(2026, 1, 15))
    summer = sun_data(34.18, -118.31, date(2026, 7, 15))
    assert _dark_hours(winter) > _dark_hours(summer)

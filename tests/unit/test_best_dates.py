from datetime import date

from src.services.astronomy import best_dates


def test_best_dates_returns_correct_count():
    result = best_dates(34.18, -118.31, date(2026, 5, 10), days=7)
    assert result.days_checked == 7
    assert len(result.nights) == 7


def test_best_dates_sorted_by_quality():
    result = best_dates(34.18, -118.31, date(2026, 5, 10), days=14)
    order = {"excellent": 0, "good": 1, "fair": 2, "poor": 3}
    scores = [order[n.quality] for n in result.nights]
    assert scores == sorted(scores)


def test_best_dates_illumination_range():
    result = best_dates(34.18, -118.31, date(2026, 5, 10), days=7)
    for night in result.nights:
        assert 0.0 <= night.moon_illumination <= 100.0


def test_best_dates_dark_hours_non_negative():
    result = best_dates(34.18, -118.31, date(2026, 5, 10), days=7)
    for night in result.nights:
        assert night.astronomical_dark_hours >= 0.0

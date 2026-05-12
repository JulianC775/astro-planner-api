import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app

BASE = "http://test"


@pytest.fixture
def transport():
    return ASGITransport(app=app)


async def test_moon_endpoint(transport):
    async with AsyncClient(transport=transport, base_url=BASE) as client:
        resp = await client.get("/moon?lat=34.18&lon=-118.31&date=2026-05-10")
    assert resp.status_code == 200
    data = resp.json()
    assert "phase_name" in data
    assert 0.0 <= data["illumination"] <= 100.0


async def test_sun_endpoint(transport):
    async with AsyncClient(transport=transport, base_url=BASE) as client:
        resp = await client.get("/sun?lat=34.18&lon=-118.31&date=2026-05-10")
    assert resp.status_code == 200
    data = resp.json()
    assert "sunrise" in data
    assert "astronomical_twilight_begin" in data


async def test_plan_endpoint(transport):
    async with AsyncClient(transport=transport, base_url=BASE) as client:
        resp = await client.get("/plan?lat=34.18&lon=-118.31&date=2026-05-10")
    assert resp.status_code == 200
    data = resp.json()
    assert "moon" in data
    assert "shooting_window" in data
    assert data["shooting_window"]["quality"] in ("excellent", "good", "fair", "poor")


async def test_best_dates_endpoint(transport):
    async with AsyncClient(transport=transport, base_url=BASE) as client:
        resp = await client.get("/best-dates?lat=34.18&lon=-118.31&days=5")
    assert resp.status_code == 200
    data = resp.json()
    assert data["days_checked"] == 5
    assert len(data["nights"]) == 5


async def test_best_dates_days_capped_at_90(transport):
    async with AsyncClient(transport=transport, base_url=BASE) as client:
        resp = await client.get("/best-dates?lat=34.18&lon=-118.31&days=200")
    assert resp.status_code == 422

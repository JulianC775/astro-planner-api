"""Integration test for the /health endpoint."""

import pytest
import httpx
from httpx import ASGITransport

from src.main import app


@pytest.mark.asyncio
async def test_health_returns_200_and_ok() -> None:
    """GET /health should return HTTP 200 with body {"status": "ok"}."""
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

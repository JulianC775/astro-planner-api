# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`astro-planner-api` is a FastAPI REST API that returns astronomical planning data (moon phase, sun events, twilight windows, Milky Way visibility, light pollution) for a given location and date. See [TECH_STACK.md](TECH_STACK.md) for library choices and architectural decisions.

## Commands

```bash
# install dependencies
uv sync

# dev server (auto-reload)
uv run fastapi dev src/main.py

# run all tests
uv run pytest

# run a single test file or test
uv run pytest tests/unit/test_moon.py
uv run pytest tests/unit/test_moon.py::test_phase_name

# lint / format
uv run ruff check .
uv run ruff format .

# type check
uv run mypy src/
```

## Architecture

The app follows a **router → service → external library** pattern:

- `src/routers/` — thin FastAPI route handlers; parse/validate query params, call a service, return the response model
- `src/services/` — all business logic; astronomical calculations (Ephem/Astropy), external API calls (light pollution), no FastAPI imports
- `src/models/` — Pydantic v2 schemas for request query params and response bodies
- `src/core/` — app config (settings loaded from `.env`), shared utilities

Every endpoint accepts `lat: float`, `lon: float`, and `date: date` as query parameters. The `/plan` endpoint is an aggregator — it calls the other services and combines their results into a single response.

Services must remain independent of each other so the `/plan` endpoint can call them concurrently with `asyncio.gather`.

## Key Conventions

- All times in responses are **UTC ISO 8601**.
- Use `async def` for route handlers and any service function that calls an external API. Pure astronomical math functions can be `def`.
- External API keys and base URLs live in `src/core/config.py` via `pydantic-settings`; never hardcode them.
- Integration tests use `httpx.AsyncClient` with FastAPI's `TestClient`/`ASGITransport` — no live network calls in CI.

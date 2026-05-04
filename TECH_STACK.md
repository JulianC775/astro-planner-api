# Tech Stack

## Core

| Layer | Choice | Reason |
|-------|--------|--------|
| Language | Python 3.12+ | Best ecosystem for astronomical/scientific libraries |
| Framework | [FastAPI](https://fastapi.tiangolo.com/) | Async, auto-generates OpenAPI docs, type-safe via Pydantic |
| Package manager | [uv](https://github.com/astral-sh/uv) | Fast, modern Python tooling with lockfile support |

## Astronomical Calculations

| Library | Purpose |
|---------|---------|
| [Astropy](https://www.astropy.org/) | Core astronomical calculations — coordinates, time, solar system bodies |
| [Ephem](https://rhodesmill.org/pyephem/) | Rise/set times, moon phase, planetary positions (lightweight alternative to Astropy for basic ephemeris) |
| [Skyfield](https://rhodesmill.org/skyfield/) | High-precision positions if needed beyond Ephem/Astropy |

> **Decision point:** Start with Ephem for speed and simplicity. Move to Astropy/Skyfield if precision requirements or Milky Way galactic coordinate math demands it.

## Light Pollution

| Approach | Notes |
|----------|-------|
| [Light Pollution Map API](https://www.lightpollutionmap.info/) | Third-party tile/data service — simplest path |
| VIIRS/NASA data | Raw satellite data, fully offline, more work to integrate |
| [darksky.net equivalent](https://github.com/djlorenz/darksky) | SQM estimates from open datasets |

> **Decision point:** Start with a third-party API call; swap in local data processing if rate limits or data freshness become a concern.

## Data & Validation

| Library | Purpose |
|---------|---------|
| [Pydantic v2](https://docs.pydantic.dev/) | Request/response validation and serialization (built into FastAPI) |
| [geopy](https://geopy.readthedocs.io/) | Reverse geocoding (coordinate → place name) if needed |

## Dev Tooling

| Tool | Purpose |
|------|---------|
| [pytest](https://pytest.org/) | Unit and integration testing |
| [httpx](https://www.python-httpx.org/) | Async test client for FastAPI endpoints |
| [Ruff](https://docs.astral.sh/ruff/) | Linting + formatting (replaces flake8, isort, black) |
| [mypy](https://mypy.readthedocs.io/) | Static type checking |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | Environment variable management |

## Project Layout (planned)

```
astro-planner-api/
├── src/
│   ├── main.py           # FastAPI app entry point
│   ├── routers/          # One file per feature area (moon, sun, milkyway, etc.)
│   ├── services/         # Business logic — astronomical calculations, external API calls
│   ├── models/           # Pydantic request/response schemas
│   └── core/             # Config, shared utilities
├── tests/
│   ├── unit/             # Pure function tests for services
│   └── integration/      # HTTP-level tests via TestClient
├── pyproject.toml        # Project metadata and dependencies
├── .env.example          # Required environment variables
├── CLAUDE.md
├── TECH_STACK.md
└── README.md
```

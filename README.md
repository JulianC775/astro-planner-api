# astro-planner-api

REST API for planning astrophotography and stargazing sessions. Given a location and date, it returns everything you need to decide when and where to shoot: moon phases, sunset/sunrise times, astronomical twilight windows, Milky Way visibility, and light pollution data.

## Features

- **Moon phase & illumination** — phase name, illumination percentage, rise/set times
- **Sun events** — sunrise, sunset, civil/nautical/astronomical twilight
- **Milky Way visibility** — optimal viewing windows based on galactic core altitude and darkness
- **Light pollution** — Bortle scale estimate and sky brightness (SQM) for a given coordinate
- **Session planning** — combined endpoint that returns a full go/no-go summary for a night

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

```bash
git clone https://github.com/JulianC775/astro-planner-api.git
cd astro-planner-api

# using uv
uv sync

# or using pip
pip install -r requirements.txt
```

### Running the API

```bash
# development server with auto-reload
uv run fastapi dev src/main.py

# production
uv run fastapi run src/main.py
```

The API will be available at `http://localhost:8000`. Interactive docs are at `/docs`.

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/moon` | Moon phase and rise/set for a location and date |
| GET | `/sun` | Sun events and twilight windows |
| GET | `/milkyway` | Milky Way visibility windows |
| GET | `/pollution` | Light pollution data for coordinates |
| GET | `/plan` | Full session plan combining all data |

All endpoints accept `lat`, `lon`, and `date` (ISO 8601) as query parameters.

## Development

```bash
# run tests
uv run pytest

# lint and format
uv run ruff check .
uv run ruff format .

# type checking
uv run mypy src/
```

See [TECH_STACK.md](TECH_STACK.md) for library choices and architectural decisions.

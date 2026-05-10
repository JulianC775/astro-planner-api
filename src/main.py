from fastapi import FastAPI

from src.routers import best_dates, milkyway, moon, plan, pollution, sun

app = FastAPI(
    title="Astro Planner API",
    version="0.1.0",
)

app.include_router(moon.router)
app.include_router(sun.router)
app.include_router(milkyway.router)
app.include_router(pollution.router)
app.include_router(plan.router)
app.include_router(best_dates.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

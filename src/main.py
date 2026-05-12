from fastapi import FastAPI

from src.routers import milkyway, moon, plan, pollution, sun

app = FastAPI(
    title="astro-planner-api",
    description="REST API for astrophotography and stargazing session planning",
    version="0.1.0",
)

app.include_router(moon.router)
app.include_router(sun.router)
app.include_router(milkyway.router)
app.include_router(pollution.router)
app.include_router(plan.router)


@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    return {"status": "ok"}

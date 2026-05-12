from pydantic import BaseModel


class MoonResponse(BaseModel):
    phase: str
    illumination: float
    moonrise: str | None
    moonset: str | None

from datetime import datetime

from pydantic import BaseModel


class MoonResponse(BaseModel):
    phase_name: str
    illumination: float
    rise: datetime | None
    set: datetime | None

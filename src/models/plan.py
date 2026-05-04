from datetime import datetime

from pydantic import BaseModel

from src.models.milkyway import MilkyWayResponse
from src.models.moon import MoonResponse
from src.models.pollution import PollutionResponse
from src.models.sun import SunResponse


class ShootingWindow(BaseModel):
    start: datetime | None
    end: datetime | None
    quality: str


class PlanResponse(BaseModel):
    moon: MoonResponse
    sun: SunResponse
    milky_way: MilkyWayResponse
    pollution: PollutionResponse
    shooting_window: ShootingWindow

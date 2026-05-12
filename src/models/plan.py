from pydantic import BaseModel

from src.models.milkyway import MilkyWayResponse
from src.models.moon import MoonResponse
from src.models.pollution import PollutionResponse
from src.models.sun import SunResponse


class PlanResponse(BaseModel):
    moon: MoonResponse
    sun: SunResponse
    milkyway: MilkyWayResponse
    pollution: PollutionResponse
    recommendation: str

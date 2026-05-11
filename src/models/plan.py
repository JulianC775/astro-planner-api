from datetime import datetime

from pydantic import BaseModel

from src.models.apod import ApodResponse
from src.models.milkyway import MilkyWayResponse
from src.models.moon import MoonResponse
from src.models.pollution import PollutionResponse
from src.models.sun import SunResponse
from src.models.weather import WeatherResponse


class ShootingWindow(BaseModel):
    start: datetime | None
    end: datetime | None
    quality: str   # "excellent" | "good" | "fair" | "poor"
    go: bool       # simple go/no-go flag


class PlanResponse(BaseModel):
    moon: MoonResponse
    sun: SunResponse
    milky_way: MilkyWayResponse
    pollution: PollutionResponse
    weather: WeatherResponse
    apod: ApodResponse | None
    shooting_window: ShootingWindow

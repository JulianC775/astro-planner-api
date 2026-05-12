from datetime import date

from pydantic import BaseModel


class NightSummary(BaseModel):
    date: date
    moon_illumination: float
    phase_name: str
    astronomical_dark_hours: float
    milkyway_visible: bool
    quality: str


class BestDatesResponse(BaseModel):
    location: dict[str, float]
    days_checked: int
    nights: list[NightSummary]

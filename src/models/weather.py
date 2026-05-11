from pydantic import BaseModel


class WeatherResponse(BaseModel):
    cloud_cover_pct: int
    seeing: str        # "excellent" | "good" | "fair" | "poor"
    transparency: str  # "excellent" | "good" | "fair" | "poor"
    wind_speed_ms: float
    description: str

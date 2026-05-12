from pydantic import BaseModel


class SunResponse(BaseModel):
    sunrise: str | None
    sunset: str | None
    civil_dawn: str | None
    civil_dusk: str | None
    nautical_dawn: str | None
    nautical_dusk: str | None
    astronomical_dawn: str | None
    astronomical_dusk: str | None

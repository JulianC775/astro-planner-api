from datetime import datetime

from pydantic import BaseModel


class SunResponse(BaseModel):
    sunrise: datetime
    sunset: datetime
    civil_twilight_begin: datetime
    civil_twilight_end: datetime
    nautical_twilight_begin: datetime
    nautical_twilight_end: datetime
    astronomical_twilight_begin: datetime
    astronomical_twilight_end: datetime

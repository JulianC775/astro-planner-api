from datetime import date

from pydantic import BaseModel


class LocationDate(BaseModel):
    lat: float
    lon: float
    date: date

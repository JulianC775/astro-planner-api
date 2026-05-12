from datetime import datetime

from pydantic import BaseModel


class MilkyWayResponse(BaseModel):
    visible: bool
    visibility_start: datetime | None
    visibility_end: datetime | None
    peak_altitude: float | None

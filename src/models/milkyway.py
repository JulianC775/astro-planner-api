from pydantic import BaseModel


class VisibilityWindow(BaseModel):
    start: str
    end: str
    peak_altitude: float


class MilkyWayResponse(BaseModel):
    visible: bool
    windows: list[VisibilityWindow]
    galactic_core_max_altitude: float

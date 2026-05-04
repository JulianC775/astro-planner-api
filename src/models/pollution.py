from pydantic import BaseModel


class PollutionResponse(BaseModel):
    bortle_class: int
    sqm: float | None
    description: str

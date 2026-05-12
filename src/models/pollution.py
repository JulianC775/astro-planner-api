from pydantic import BaseModel


class PollutionResponse(BaseModel):
    bortle_class: int | None
    sqm: float | None
    description: str

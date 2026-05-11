from pydantic import BaseModel


class ApodResponse(BaseModel):
    date: str
    title: str
    explanation: str
    url: str
    media_type: str   # "image" | "video"
    hdurl: str | None

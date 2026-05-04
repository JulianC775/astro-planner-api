from src.models.pollution import PollutionResponse


async def get_pollution(lat: float, lon: float) -> PollutionResponse:
    # TODO: Integrate with a real light pollution API (e.g. lightpollutionmap.info)
    # using settings.light_pollution_api_key. For now return a placeholder.
    return PollutionResponse(
        bortle_class=5,
        sqm=20.5,
        description="Suburban sky",
    )

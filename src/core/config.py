from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    pollution_api_url: str = "https://www.lightpollutionmap.info/QueryRaster/"


settings = Settings()

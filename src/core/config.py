from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Get a free key at https://api.nasa.gov — falls back to DEMO_KEY if unset
    apod_api_key: str = ""


settings = Settings()

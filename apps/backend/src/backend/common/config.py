from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class CustomBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parents[3] / ".env",  # backend root .env file
        env_file_encoding="utf-8",
        extra="ignore",
    )

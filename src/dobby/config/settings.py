from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    name: str = "dobby"
    environment: str = "development"


class RuntimeSettings(BaseModel):
    log_level: str = "INFO"


class PathSettings(BaseModel):
    model_store: Path = Path("/P/dobby/models")
    dataset_store: Path = Path("/P/dobby/datasets")
    cache_store: Path = Path("/P/dobby/cache")


class DobbySettings(BaseSettings):
    app: AppSettings = Field(default_factory=AppSettings)
    runtime: RuntimeSettings = Field(default_factory=RuntimeSettings)
    paths: PathSettings = Field(default_factory=PathSettings)

    model_config = SettingsConfigDict(
        env_prefix="DOBBY_",
        env_nested_delimiter="__",
        extra="ignore",
    )

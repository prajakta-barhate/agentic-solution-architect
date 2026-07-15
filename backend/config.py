from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE)


def _env_value(key: str, default: str | None = None) -> str | None:
    value = os.getenv(key, default)
    if value is None:
        return None
    value = value.strip()
    return value or None


def _parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return default


class Settings(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra="ignore")

    app_name: str = Field(default="Agentic Solution Architect API")
    environment: Literal["development", "production"] = Field(default="development")
    debug: bool = Field(default=False)
    api_v1_prefix: str = Field(default="/api/v1")
    database_url: str = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/agentic_architect"
    )
    gemini_api_key: str | None = Field(default=None)
    secret_key: str | None = Field(default=None)

    @classmethod
    def from_env(cls) -> "Settings":
        environment = _env_value("ENVIRONMENT", "development")
        if environment not in {"development", "production"}:
            raise ValueError("ENVIRONMENT must be either 'development' or 'production'")

        return cls(
            app_name=_env_value("APP_NAME", "Agentic Solution Architect API") or "Agentic Solution Architect API",
            environment=environment,
            debug=_parse_bool(_env_value("DEBUG", "false"), default=False),
            api_v1_prefix=_env_value("API_V1_PREFIX", "/api/v1") or "/api/v1",
            database_url=_env_value(
                "DATABASE_URL",
                "postgresql+psycopg2://postgres:postgres@localhost:5432/agentic_architect",
            )
            or "postgresql+psycopg2://postgres:postgres@localhost:5432/agentic_architect",
            gemini_api_key=_env_value("GEMINI_API_KEY"),
            secret_key=_env_value("SECRET_KEY"),
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings.from_env()


settings = get_settings()

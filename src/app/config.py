import logging
import os
from functools import lru_cache

from pydantic import AnyUrl, BaseSettings

logger_name = "uvicorn"
log = logging.getLogger(logger_name)


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", 0)
    database_url: AnyUrl = os.environ.get("DATABASE_URL")
    token_validity_minutes: int = os.getenv("TOKEN_VALIDITY_MINUTES", 30)
    secret_key: str = os.getenv("TOKEN_SECRET_KEY", "hemlis")


@lru_cache()
def get_settings() -> Settings:
    log.info("Loading config settings from the environment...")
    return Settings()

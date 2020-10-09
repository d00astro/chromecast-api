import logging
import os
from functools import lru_cache

from pydantic import AnyUrl, BaseSettings

logger_name = "uvicorn"
log = logging.getLogger(logger_name)


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", 0)
    route_prefix: str = os.getenv("ROUTE_PREFIX", "/home")
    version: str = os.getenv("VERSION", "0.0.1")

@lru_cache()
def get_settings() -> Settings:
    log.info("Loading config settings from the environment...")
    return Settings()

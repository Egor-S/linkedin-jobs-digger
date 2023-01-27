from pathlib import Path
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    db_uri: str = "sqlite:///jobs.sqlite"


MODULE_ROOT = Path(__file__).parent.resolve()


@lru_cache()
def get_settings():
    return Settings()

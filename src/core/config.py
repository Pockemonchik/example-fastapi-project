import os
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    mode: str = os.environ.get("MODE", "DEV")

    postgres_url: str = os.environ.get("DB_URL", "locahost")
    postgres_echo: bool = bool(os.environ.get("DB_ECHO", False))

    mongo_url: str = os.environ.get("MONGO_CONNECTION_URL", "mongodb://localhost:27017/")
    mongo_db_name: str = os.environ.get("MONGO_DATABASE_NAME", "example_app")


def get_settings():
    return Settings()

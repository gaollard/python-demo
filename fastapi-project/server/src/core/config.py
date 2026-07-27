from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILE = Path(__file__).resolve().parent.parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_username: str = "root"
    db_password: str = ""
    db_database: str = "forum"

    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24

    app_title: str = "Forum API"
    app_version: str = "0.1.0"

    # Local media uploads (relative to server/ by default)
    upload_dir: str = "uploads"
    media_url_prefix: str = "/media"
    upload_max_files: int = 9
    upload_max_bytes: int = 5 * 1024 * 1024  # 5MB


@lru_cache
def get_settings() -> Settings:
    return Settings()

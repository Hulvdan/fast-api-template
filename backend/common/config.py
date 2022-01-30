"""Конфигурация приложения на основе констант и переменных окружения."""
from pathlib import Path

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).parent.parent.parent


class AppConfig(BaseSettings):
    """Конфигурация приложения."""

    class Config:  # noqa: D106
        env_file = ".env"
        env_file_encoding = "utf-8"

    project_name: str = Field(env="PROJECT_NAME", default="backend")
    cors_origins: str = Field(env="BACKEND_CORS_ORIGINS", default="")
    sentry_dsn = Field(env="SENTRY_DSN", default="")
    base_dir = BASE_DIR
    apps: list[str] = [
        "health_check",
        "upload_file",
    ]


class DatabaseConfig(BaseSettings):
    """Конфигурация БД."""

    class Config:  # noqa: D106
        env_file = ".env"
        env_file_encoding = "utf-8"

    protocol: str = "postgresql+asyncpg"
    database: str = Field(env="POSTGRES_DB")
    username: str = Field(env="POSTGRES_USER")
    password: str = Field(env="POSTGRES_PASSWORD")
    host: str = Field(env="BACKEND_DATABASE_HOST")
    port: int = Field(env="BACKEND_DATABASE_PORT", cast=int)

    @property
    def database_url(self) -> str:
        """URL подключения к БД."""
        return "{protocol}://{username}:{password}@{host}:{port}/{database}".format(
            protocol=self.protocol,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )


class AWSConfig(BaseSettings):
    """Конфигурация S3."""

    class Config:  # noqa: D106
        env_file = ".env"
        env_file_encoding = "utf-8"

    access_key_id: str = Field(env="AWS_ACCESS_KEY_ID")
    secret_access_key: str = Field(env="AWS_SECRET_ACCESS_KEY")
    storage_bucket_name: str = Field(env="AWS_STORAGE_BUCKET_NAME")
    endpoint_url: str = Field(env="AWS_S3_ENDPOINT_URL")


__all__ = [
    "AWSConfig",
    "AppConfig",
    "DatabaseConfig",
]

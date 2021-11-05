"""
Контейнер конфигурации приложения.

Руководствовался методологией разработки "The Twelve-Factor App".
Пунктом - III. Конфигурация. https://12factor.net/ru/config.

Конфигурация должна задаваться в первую очередь переменными окружения.
Для локальной разработки можно добавить декларативные файлы (.env в корне сервиса).

Такой подход был вдохновлён шаблоном "wemake-django-template".
https://github.com/wemake-services/wemake-django-template.
"""
import os
from datetime import timedelta
from pathlib import Path
from typing import cast

from decouple import AutoConfig
from dependency_injector import containers, providers

# Loading `.env` files
# See docs: https://gitlab.com/mkleehammer/autoconfig
BASE_DIR = Path(__file__).parent.parent.parent
config: AutoConfig = AutoConfig(search_path=BASE_DIR)


class AppConfig:
    apps: list[str] = [
        "health_check",
        "token",
        "hello_world",
    ]
    project_name: str = config("PROJECT_NAME", default="backend")
    cors_origins: str = config("BACKEND_CORS_ORIGINS", default="")
    sentry_dsn = config("SENTRY_DSN", default="")
    base_dir = BASE_DIR


class AuthConfig:
    jwt_expiration_delta = timedelta(
        hours=config("ACCESS_TOKEN_EXPIRE_MINUTES", default=10, cast=int)  # in hours
    )
    jwt_refresh_expiration_delta = timedelta(
        hours=config("JWT_REFRESH_EXPIRATION_DELTA", default=10, cast=int)  # in hours
    )
    jwt_auth_header_prefix = config("JWT_AUTH_HEADER_PREFIX", default="JWT")
    jwt_secret_key: str = cast(str, providers.Dependency())
    oauth_scopes = {"read": "Read", "write": "Write"}
    secret_key = config("BACKEND_SECRET_KEY", default=os.urandom(32))


class DatabaseConfig:
    type = "postgresql+asyncpg"
    database: str = config("POSTGRES_DB")
    username: str = config("POSTGRES_USER")
    password: str = config("POSTGRES_PASSWORD")
    host: str = config("BACKEND_DATABASE_HOST")
    port: int = config("BACKEND_DATABASE_PORT", cast=int)

    @property
    def database_url(self) -> str:
        return "{type}://{username}:{password}@{host}:{port}/{database}".format(
            type=self.type,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )


class StorageConfig:
    s3_endpoint_url: str = config("S3_ENDPOINT_URL", default="")
    s3_storage_bucket_name: str = config("S3_STORAGE_BUCKET_NAME", default="")
    s3_access_key_id: str = config("S3_ACCESS_KEY_ID", default="")
    s3_secret_access_key: str = config("S3_SECRET_ACCESS_KEY", default="")
    s3_storage_enabled: bool = (
        bool(s3_endpoint_url)
        and bool(s3_storage_bucket_name)
        and bool(s3_access_key_id)
        and bool(s3_secret_access_key)
    )


class EmailConfig:
    smtp_tls: bool = config("SMTP_TLS", default=True, cast=bool)
    smtp_port: int = config("SMTP_PORT", default=0, cast=int)
    smtp_host: str = config("SMTP_HOST", default="")
    smtp_user: str = config("SMTP_USER", default="")
    smtp_password: str = config("SMTP_PASSWORD", default="")

    emails_from_email: str = config(
        "EMAILS_FROM_EMAIL", default=config("PROJECT_NAME", default="backend")
    )
    emails_from_name: str = cast(str, providers.Dependency())
    email_reset_token_expire_hours: int = 48
    email_templates_dir: str = "/app/app/email-templates/build"
    emails_enabled: bool = bool(smtp_host) and bool(smtp_port) and bool(emails_from_email)


class Config(containers.DeclarativeContainer):
    app = providers.Object(AppConfig())
    auth = providers.Object(AuthConfig())
    database = providers.Object(DatabaseConfig())
    storage = providers.Object(StorageConfig())
    email = providers.Object(EmailConfig())

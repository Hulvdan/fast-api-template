from pathlib import Path

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).parent.parent.parent


class AppConfig(BaseSettings):
    project_name: str = Field(env="PROJECT_NAME", default="backend")
    cors_origins: str = Field(env="BACKEND_CORS_ORIGINS", default="")
    sentry_dsn = Field(env="SENTRY_DSN", default="")
    base_dir = BASE_DIR
    apps: list[str] = [
        "health_check",
        "token",
        "hello_world",
    ]


class AuthConfig(BaseSettings):
    jwt_expiration_delta = Field(env="ACCESS_TOKEN_EXPIRE_MINUTES", default=600)
    jwt_refresh_expiration_delta = Field(env="JWT_REFRESH_EXPIRATION_DELTA", default=10)
    jwt_auth_header_prefix = Field(env="JWT_AUTH_HEADER_PREFIX", default="JWT")
    jwt_secret_key: str = Field(env="JWT_SECRET_KEY", default="dumb_secret_key")
    oauth_scopes = {"read": "Read", "write": "Write"}
    secret_key = Field(env="BACKEND_SECRET_KEY", default="dumb_secret_key")


class DatabaseConfig(BaseSettings):
    type = "postgresql+asyncpg"
    database: str = Field(env="POSTGRES_DB")
    username: str = Field(env="POSTGRES_USER")
    password: str = Field(env="POSTGRES_PASSWORD")
    host: str = Field(env="BACKEND_DATABASE_HOST")
    port: int = Field(env="BACKEND_DATABASE_PORT", cast=int)

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

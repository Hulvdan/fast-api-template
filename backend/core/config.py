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
        "hello_world",
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class AuthConfig(BaseSettings):
    jwt_expiration_delta = Field(env="ACCESS_TOKEN_EXPIRE_MINUTES", default=600)
    jwt_refresh_expiration_delta = Field(env="JWT_REFRESH_EXPIRATION_DELTA", default=10)
    jwt_auth_header_prefix = Field(env="JWT_AUTH_HEADER_PREFIX", default="JWT")
    jwt_secret_key: str = Field(env="JWT_SECRET_KEY", default="dumb_secret_key")
    oauth_scopes = {"read": "Read", "write": "Write"}
    secret_key = Field(env="BACKEND_SECRET_KEY", default="dumb_secret_key")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


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

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class AWSSettings(BaseSettings):
    access_key_id: str = Field(env="AWS_ACCESS_KEY_ID")
    secret_access_key: str = Field(env="AWS_SECRET_ACCESS_KEY")
    storage_bucket_name: str = Field(env="AWS_STORAGE_BUCKET_NAME")
    endpoint_url: str = Field(env="AWS_S3_ENDPOINT_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

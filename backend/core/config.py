import os
from datetime import timedelta
from pathlib import Path

from decouple import AutoConfig

# PATH
BASE_DIR = Path(__file__).parent.parent

# Loading `.env` files
# See docs: https://gitlab.com/mkleehammer/autoconfig
config: AutoConfig = AutoConfig(search_path=BASE_DIR)


class Config:
    TEST = {
        "database": "test_default",
    }

    _DATABASES = {
        "type": "",
        "username": "",
        "password": "",
        "host": "",
        "port": "",
        "database": "",
    }


# TEST
TEST_RUN = config("TEST_RUN", default=False, cast=bool)


# SECRET
SECRET_KEY = config("SECRET_KEY", default=os.urandom(32))


# APPS
APPS = ["health_check", "token", "hello_world"]


# JWT
JWT_EXPIRATION_DELTA = timedelta(
    hours=config("ACCESS_TOKEN_EXPIRE_MINUTES", default=10, cast=int)  # in hours
)
JWT_REFRESH_EXPIRATION_DELTA = timedelta(
    hours=config("JWT_REFRESH_EXPIRATION_DELTA", default=10, cast=int)  # in hours
)
JWT_AUTH_HEADER_PREFIX = config("JWT_AUTH_HEADER_PREFIX", default="JWT")
JWT_SECRET_KEY = SECRET_KEY


# CORS
# a string of origins separated by commas, e.g:
# 'http://localhost, http://localhost:4200, http://localhost:3000'
BACKEND_CORS_ORIGINS = config("BACKEND_CORS_ORIGINS", default="")


# APP
PROJECT_NAME = config("PROJECT_NAME", default="backend")


# EMAIL
SENTRY_DSN = config("SENTRY_DSN", default="")

SMTP_TLS = config("SMTP_TLS", default=True, cast=bool)
SMTP_PORT = config("SMTP_PORT", default=0, cast=int)
SMTP_HOST = config("SMTP_HOST", default="")
SMTP_USER = config("SMTP_USER", default="")
SMTP_PASSWORD = config("SMTP_PASSWORD", default="")

EMAILS_FROM_EMAIL = config("EMAILS_FROM_EMAIL", default="")
EMAILS_FROM_NAME = PROJECT_NAME
EMAIL_RESET_TOKEN_EXPIRE_HOURS = 48
EMAIL_TEMPLATES_DIR = "/app/app/email-templates/build"
EMAILS_ENABLED = SMTP_HOST and SMTP_PORT and EMAILS_FROM_EMAIL


# DATABASE
DATABASES = {
    "type": "postgresql",
    "database": config("POSTGRES_DB"),
    "username": config("POSTGRES_USER"),
    "password": config("POSTGRES_PASSWORD"),
    "host": config("BACKEND_DATABASE_HOST"),
    "port": config("BACKEND_DATABASE_PORT"),
}

# OAUTH 2
SCOPES = {"read": "Read", "write": "Write"}

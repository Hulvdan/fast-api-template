"""Создание и конфигурация FastAPI приложения."""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, PlainTextResponse

from application.common.container import get_container
from common.base import DomainException
from common.config import AppConfig

from .base import HttpExceptionMeta


def add_cors_middleware(app: FastAPI, app_config: AppConfig) -> None:
    """Добавление разрешённых хостов в заголовок CORS_ORIGINS."""
    origins = []
    if app_config.cors_origins:
        origins_raw = app_config.cors_origins.split(",")
        for origin in origins_raw:
            use_origin = origin.strip()
            origins.append(use_origin)
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


async def create_app() -> FastAPI:
    """Создание и конфигурация FastAPI приложения."""
    from . import urls

    container = get_container()
    container.finalize()  # Закрываем DI контейнер для изменений

    app_config = container.resolve(AppConfig)
    app = FastAPI(title=app_config.project_name)
    app.include_router(urls.router)
    add_cors_middleware(app, app_config)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: Exception) -> PlainTextResponse:
        return PlainTextResponse(str(exc), status_code=400)

    @app.exception_handler(DomainException)
    async def domain_exception_handler(_: Request, exc: DomainException) -> JSONResponse:
        http_exception = HttpExceptionMeta.registered_exceptions[exc.__class__]
        return JSONResponse(
            {
                "message": http_exception.message,
                "reason": http_exception.reason,
            },
            status_code=http_exception.status,
        )

    return app

"""Создание и конфигурация FastAPI приложения."""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse

from application.common.container import get_container
from common.config import Config


def add_cors_middleware(app: FastAPI, config: Config) -> None:
    """Добавление разрешённых хостов в заголовок CORS_ORIGINS."""
    app_config = config.app

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

    config = container.resolve(Config)
    app = FastAPI(title=config.app.project_name)
    app.include_router(urls.router)
    add_cors_middleware(app, config)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: Exception) -> PlainTextResponse:
        return PlainTextResponse(str(exc), status_code=400)

    return app

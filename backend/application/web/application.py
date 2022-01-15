from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse

from common.config import AppConfig
from common.container import get_container


def add_cors_middleware(app: FastAPI, app_config: AppConfig) -> None:
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
    from . import urls

    container = get_container()
    container.finalize()  # Закрываем DI контейнер для изменений

    app = FastAPI(title=container.resolve(AppConfig).project_name)
    app.include_router(urls.router)
    add_cors_middleware(app, container.resolve(AppConfig))

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: Exception) -> PlainTextResponse:
        return PlainTextResponse(str(exc), status_code=400)

    return app

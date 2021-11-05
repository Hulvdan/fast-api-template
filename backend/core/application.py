import sys

from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse

from core.containers.config import AppConfig

from .containers import Container


@inject
def add_cors_middleware(
    app: FastAPI, app_config: AppConfig = Provide[Container.config.app]
) -> None:
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
    container = Container()
    from . import urls

    container.wire(
        modules=[
            sys.modules[__name__],
        ],
        packages=[
            sys.modules["apps"],
        ],
    )

    db = container.resources.db()
    await db.create_database()

    app = FastAPI(title=container.config.app.provided.project_name())
    app.include_router(urls.router)
    add_cors_middleware(app)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: Exception) -> PlainTextResponse:
        return PlainTextResponse(str(exc), status_code=400)

    return app

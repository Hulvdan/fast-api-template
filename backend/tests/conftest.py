import asyncio
import io
import logging
import os
from typing import Callable

import httpx
from PIL import Image
from pytest import fixture
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import AuthConfig
from core.resources.database import DatabaseResource
from libs.punq import Container

logger = logging.getLogger("fixture")
logger.setLevel(logging.INFO)


def pytest_sessionstart():
    os.environ["POSTGRES_DB"] = "postgres_test"


@fixture(scope="session")
def container() -> Container:
    from core.container import initialize_container

    container = initialize_container()
    container.finalize()
    return container


@fixture(scope="session", autouse=True)
def db(container) -> None:
    """Инициализация БД для тестов.

    Создание БД при старте тестов и удаление при завершении.
    """
    db: DatabaseResource = container.resolve(DatabaseResource)
    db.drop_database()
    db.create_database()
    yield
    db.drop_database()


@fixture(scope="session")
def auth_config(container: Container) -> AuthConfig:
    return container.resolve(AuthConfig)


@fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    return asyncio.get_event_loop()


@fixture(scope="function")
async def client() -> httpx.AsyncClient:
    from core.application import create_app

    app = await create_app()
    async with httpx.AsyncClient(base_url="http://localhost:8000", app=app) as client:
        yield client


@fixture(scope="function")
def image_factory() -> Callable[..., io.BytesIO]:
    def get_image(image_name) -> io.BytesIO:
        file = io.BytesIO()
        image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
        image.save(file, "png")
        file.name = image_name
        file.seek(0)
        return file

    return get_image

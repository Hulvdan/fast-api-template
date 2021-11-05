import asyncio
import io
import logging
import os
from typing import Callable

import httpx
from PIL import Image
from pytest import fixture
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger("fixture")
logger.setLevel(logging.INFO)


def pytest_sessionstart():
    os.environ.setdefault("POSTGRES_DB", "backendtest")
    from core.containers import Container


@fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@fixture(scope="function")
async def session() -> AsyncSession:
    from core.containers import Container

    async with Container.resources.db().session() as session:
        yield session


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

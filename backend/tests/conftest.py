import asyncio
import io
import logging
import os
from typing import AsyncGenerator, Callable, Generator, Union

import httpx
from PIL import Image  # type: ignore[import]
from pytest import fixture

from common.config import AuthConfig
from common.resources.database import DatabaseResource
from common.services.implementations.storage_mock import StorageMock
from common.services.interfaces.storage import IAsyncFile, IStorage
from libs.punq import Container

logger = logging.getLogger("fixture")
logger.setLevel(logging.INFO)


def pytest_sessionstart() -> None:
    os.environ["POSTGRES_DB"] = "postgres_test"


@fixture(scope="session")
def container() -> Container:
    """Тут мы переопределяем сервисы на моки.

    Например, смс-ки, email-ы, файлы и т.п.
    """
    from common.container import get_container

    container = get_container()

    container.purge(IStorage)
    container.register(IStorage, StorageMock)  # type: ignore[misc]

    container.finalize()
    return container


@fixture(scope="session", autouse=True)
def db(container: Container) -> Generator[None, None, None]:
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
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    from application.web.application import create_app

    app = await create_app()
    async with httpx.AsyncClient(base_url="http://localhost:8000", app=app) as client:
        yield client


@fixture(scope="function")
def image_factory() -> Callable[[str], io.BytesIO]:
    def get_image(image_name: str) -> io.BytesIO:
        file = io.BytesIO()
        image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
        image.save(file, "png")
        file.name = image_name
        file.seek(0)
        return file

    return get_image


class AsyncImage:
    def __init__(self, file: io.BytesIO) -> None:
        self._file = file

    async def write(self, data: Union[bytes, str]) -> None:
        self._file.write(data)  # type: ignore

    async def read(self, size: int = -1) -> Union[bytes, str]:
        return self._file.read(size)

    async def seek(self, offset: int) -> None:
        self._file.seek(offset)

    async def close(self) -> None:
        self._file.close()


@fixture(scope="function")
def async_file_factory() -> Callable[[str], IAsyncFile]:
    def get_async_file(file_name: str) -> IAsyncFile:
        file = io.BytesIO()
        image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
        image.save(file, "png")
        file.name = file_name
        file.seek(0)
        return AsyncImage(file)

    return get_async_file

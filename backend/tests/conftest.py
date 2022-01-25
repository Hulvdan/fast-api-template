import asyncio
import io
import os
from typing import AsyncGenerator, Callable, Generator, Union

import httpx
import pytest
from PIL import Image  # type: ignore[import]

from common.resources.database import DatabaseResource
from common.services.storage import IAsyncFile, IStorage
from infrastructure.services.storage_mock import StorageMock
from libs.punq import Container


def pytest_sessionstart() -> None:
    """Подмена названия БД при запуске тестов."""
    os.environ["POSTGRES_DB"] = "postgres_test"


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session", autouse=True)
def _db(container: Container) -> Generator[None, None, None]:
    """Инициализация БД для тестов.

    Создание БД при старте тестов и удаление при завершении.
    """
    db: DatabaseResource = container.resolve(DatabaseResource)
    db.drop_database()
    db.create_database()
    yield
    db.drop_database()


@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    """Фикстура event-loop-а. Нужна для работы python-asyncio."""
    return asyncio.get_event_loop()


@pytest.fixture()
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Фикстура HTTP клиента."""
    from application.web.application import create_app

    app = await create_app()
    async with httpx.AsyncClient(base_url="http://localhost:8000", app=app) as client:
        yield client


@pytest.fixture()
def image_factory() -> Callable[[str], io.BytesIO]:
    """Фикстура фабрики синхронных бинарных потоков."""

    def _get_image(image_name: str) -> io.BytesIO:
        file = io.BytesIO()
        image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
        image.save(file, "png")
        file.name = image_name
        file.seek(0)
        return file

    return _get_image


class AsyncImage:
    """Эмуляция асинхронного бинарного потока."""

    def __init__(self, file: io.BytesIO) -> None:
        """Оборачивание обычного бинарного потока в виде файла."""
        self._file = file

    async def write(self, data: Union[bytes, str]) -> None:
        """Запись в бинарный поток."""
        self._file.write(data)  # type: ignore

    async def read(self, size: int = -1) -> Union[bytes, str]:
        """Чтение из бинарного потока."""
        return self._file.read(size)

    async def seek(self, offset: int) -> None:
        """Перемещение по бинарному потоку."""
        self._file.seek(offset)

    async def close(self) -> None:
        """Закрытие бинарного потока."""
        self._file.close()


@pytest.fixture()
def async_file_factory() -> Callable[[str], IAsyncFile]:
    """Фикстура фабрики асинхронных бинарных потоков."""

    def _get_async_file(file_name: str) -> IAsyncFile:
        file = io.BytesIO()
        image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
        image.save(file, "png")
        file.name = file_name
        file.seek(0)
        return AsyncImage(file)

    return _get_async_file

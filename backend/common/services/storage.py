"""Интерфейс сервиса, взаимодействующим с хранилищем файлов."""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import NamedTuple, Protocol, Union

from common.config import Config
from common.services.random_re import IRandomRe


class FileMeta(NamedTuple):
    """Метаданные файлов, загруженных в хранилище."""

    url: str
    key: str
    filename: str
    last_modified: datetime
    content_length: int
    upload_path: str


class IAsyncFile(Protocol):
    """Протокол асинхронных бинарных потоков для файлов."""

    filename: str

    async def write(self, data: Union[bytes, str]) -> None:
        """Запись в поток."""

    async def read(self, size: int = -1) -> Union[bytes, str]:
        """Чтение из потока."""

    async def seek(self, offset: int) -> None:
        """Перемещение позиции в потоке."""

    async def close(self) -> None:
        """Закрытие потока."""


class IStorage(ABC):
    """Интерфейс сервиса, взаимодействующим с хранилищем файлов."""

    @abstractmethod
    def __init__(self, config: Config, random_re: IRandomRe) -> None:
        """Создание экземпляра с сохранением конфигурации."""
        raise NotImplementedError

    @abstractmethod
    async def upload_file(self, file: IAsyncFile, upload_path: str) -> FileMeta:
        """Загрузка файла в хранилище."""
        raise NotImplementedError

    @abstractmethod
    async def delete_file(self, file_meta: FileMeta) -> None:
        """Удаление файла из хранилища."""
        raise NotImplementedError

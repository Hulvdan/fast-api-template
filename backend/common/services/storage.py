"""Интерфейс сервиса, взаимодействующим с хранилищем файлов."""
from abc import abstractmethod
from datetime import datetime
from typing import NamedTuple, Protocol, Union


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


class IStorage(Protocol):
    """Интерфейс сервиса, взаимодействующим с хранилищем файлов."""

    @abstractmethod
    async def upload_file(self, file: IAsyncFile, upload_path: str) -> FileMeta:
        """Загрузка файла в хранилище."""
        raise NotImplementedError

    @abstractmethod
    async def delete_file(self, file_meta: FileMeta) -> None:
        """Удаление файла из хранилища."""
        raise NotImplementedError

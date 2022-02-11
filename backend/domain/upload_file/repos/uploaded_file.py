"""Репозиторий и модель загруженного файла."""
from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Protocol
from uuid import UUID


@dataclass
class UploadedFile:
    """Загруженный файл."""

    url: str
    key: str
    filename: str
    last_modified: datetime
    content_length: int
    upload_path: str
    uuid: Optional[UUID] = None


class IUploadedFileRepo(Protocol):
    """Интерфейс репозиторий загруженных файлов."""

    @abstractmethod
    async def delete(self, file: UploadedFile) -> None:
        """Удаление конкретного файла."""

    @abstractmethod
    async def create(self, file: UploadedFile) -> UploadedFile:
        """Создание файла."""

    @abstractmethod
    async def get(self, uuid: UUID) -> Optional[UploadedFile]:
        """Получение конкретного файла."""


__all__ = [
    "IUploadedFileRepo",
    "UploadedFile",
]

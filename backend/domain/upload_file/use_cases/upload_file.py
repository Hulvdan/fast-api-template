"""Сценарий загрузки файла в хранилище файлов."""
from common.base import BaseUseCase
from common.services.storage import FileMeta, IAsyncFile, IStorage


class UploadFileUseCase(BaseUseCase):
    """Сценарий загрузки файла в хранилище файлов."""

    def __init__(self, storage_service: IStorage) -> None:
        """Создание экземпляра с сохранением конфигурации."""
        self.storage_service = storage_service
        self.upload_path = "h/w"

    async def execute(self, upload_file: IAsyncFile) -> FileMeta:
        """Загрузка файла в хранилище файлов."""
        return await self.storage_service.upload_file(upload_file, self.upload_path)

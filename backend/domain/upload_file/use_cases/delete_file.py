"""Сценарий загрузки файла в хранилище файлов."""
from uuid import UUID

from common.base import UseCaseMeta
from common.services.storage import FileMeta, IStorage
from domain.upload_file.exceptions import FileDoesNotExistError
from domain.upload_file.repos.uploaded_file import IUploadedFileRepo


class DeleteFileUseCase(metaclass=UseCaseMeta):
    """Сценарий удаления файла из хранилища файлов."""

    def __init__(self, storage_service: IStorage, file_repo: IUploadedFileRepo) -> None:
        """Создание экземпляра с сохранением конфигурации."""
        self._storage_service = storage_service
        self._upload_path = "h/w"
        self._file_repo = file_repo

    async def execute(self, file_uuid: UUID) -> None:
        """Удаление файла из хранилища файлов."""
        file = await self._file_repo.get(file_uuid)
        if file is None:
            raise FileDoesNotExistError()

        meta = FileMeta(
            url=file.url,
            key=file.key,
            filename=file.filename,
            last_modified=file.last_modified,
            content_length=file.content_length,
            upload_path=file.upload_path,
        )

        await self._storage_service.delete_file(meta)
        await self._file_repo.delete(file)


__all__ = [
    "DeleteFileUseCase",
]

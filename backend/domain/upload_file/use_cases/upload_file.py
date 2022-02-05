"""Сценарий загрузки файла в хранилище файлов."""
from common.base import UseCaseMeta
from common.services.storage import IAsyncFile, IStorage
from domain.upload_file.repos.uploaded_file import IUploadedFileRepo, UploadedFile


class UploadFileUseCase(metaclass=UseCaseMeta):
    """Сценарий загрузки файла в хранилище файлов."""

    def __init__(self, storage_service: IStorage, file_repo: IUploadedFileRepo) -> None:
        """Создание экземпляра с сохранением конфигурации."""
        self._storage_service = storage_service
        self._upload_path = "h/w"
        self._file_repo = file_repo

    async def execute(self, upload_file: IAsyncFile) -> UploadedFile:
        """Загрузка файла в хранилище файлов."""
        file_meta = await self._storage_service.upload_file(upload_file, self._upload_path)
        return await self._file_repo.create(
            UploadedFile(
                url=file_meta.url,
                key=file_meta.key,
                filename=file_meta.filename,
                last_modified=file_meta.last_modified,
                content_length=file_meta.content_length,
                upload_path=file_meta.upload_path,
            )
        )

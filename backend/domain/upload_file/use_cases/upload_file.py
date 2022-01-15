from common.services.interfaces.storage import FileMeta, IAsyncFile, IStorage
from core.base import BaseUseCase


class UploadFileUseCase(BaseUseCase):
    def __init__(self, storage_service: IStorage) -> None:
        self.storage_service = storage_service
        self.upload_path = "h/w"

    async def execute(self, upload_file: IAsyncFile) -> FileMeta:
        file_meta = await self.storage_service.upload_file(upload_file, self.upload_path)
        return file_meta

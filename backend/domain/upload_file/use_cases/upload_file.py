from common.base import BaseUseCase
from common.services.interfaces.storage import IAsyncFile, IStorage

from ..models import UploadFileResponse


class UploadFileUseCase(BaseUseCase):
    def __init__(self, storage_service: IStorage) -> None:
        self.storage_service = storage_service
        self.upload_path = "h/w"

    async def execute(self, upload_file: IAsyncFile) -> UploadFileResponse:
        file_meta = await self.storage_service.upload_file(upload_file, self.upload_path)
        return UploadFileResponse.parse_obj(
            dict(
                url=file_meta.url,
                key=file_meta.key,
                last_modified=file_meta.last_modified,
                content_length=file_meta.content_length,
                upload_path=file_meta.upload_path,
            )
        )

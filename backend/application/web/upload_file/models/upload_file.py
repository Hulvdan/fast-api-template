"""Модели запросов/ответов загрузки файла."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UploadFileResponse(BaseModel):
    """Ответ на запрос загрузки файла."""

    uuid: UUID
    url: str
    key: str
    last_modified: datetime
    content_length: int
    upload_path: str

"""Модели запросов/ответов загрузки файла."""
from datetime import datetime

from pydantic import BaseModel


class UploadFileResponse(BaseModel):
    """Ответ на запрос загрузки файла."""

    url: str
    key: str
    last_modified: datetime
    content_length: int
    upload_path: str

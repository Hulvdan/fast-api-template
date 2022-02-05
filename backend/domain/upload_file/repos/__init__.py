"""Репозитории и модели приложения загрузки файлов."""
from .uploaded_file import IUploadedFileRepo, UploadedFile

__all__ = [
    "IUploadedFileRepo",
    "UploadedFile",
]

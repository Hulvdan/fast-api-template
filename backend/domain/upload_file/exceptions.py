"""Доменные исключения приложения загрузки файлов."""
from common.base import DomainException


class FileDoesNotExistError(DomainException):
    """Файл не найден."""


__all__ = [
    "FileDoesNotExistError",
]

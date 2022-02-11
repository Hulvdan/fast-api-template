"""Исключения приложения загрузки файлов."""
from http import HTTPStatus

from domain.upload_file.exceptions import FileDoesNotExistError

from ..base import HttpExceptionMeta


class FileDoesNotExistHttpError(metaclass=HttpExceptionMeta):
    """Файл не найден."""

    message = "Файл не найден."
    reason = "file_does_not_exist"
    status = HTTPStatus.NOT_FOUND

    domain_exception = FileDoesNotExistError


__all__ = [
    "FileDoesNotExistHttpError",
]

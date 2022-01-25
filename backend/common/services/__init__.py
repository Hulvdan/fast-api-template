"""Интерфейсы сервисов, а также вспомогательные типы, используемые в приложении."""
from .random_re import IRandomRe
from .storage import FileMeta, IAsyncFile, IStorage

__all__ = [
    "FileMeta",
    "IAsyncFile",
    "IRandomRe",
    "IStorage",
]

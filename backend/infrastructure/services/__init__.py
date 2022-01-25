"""Сборник всех реализаций интерфейсов сервисов."""
from .random_re_rstr import RandomReXeger
from .storage_mock import StorageMock
from .storage_s3 import StorageS3

__all__ = [
    "RandomReXeger",
    "StorageMock",
    "StorageS3",
]

"""Dependency-injection контейнер."""
from functools import lru_cache

from common.base import UseCaseMeta
from common.config import AppConfig, AWSConfig, DatabaseConfig
from common.services.random_re import IRandomRe
from common.services.storage import IStorage
from domain.upload_file.repos import IUploadedFileRepo
from infrastructure.database import DatabaseResource
from infrastructure.services.random_re_rstr import RandomReXeger
from infrastructure.services.storage_s3 import StorageS3
from infrastructure.upload_file.repos import UploadedFileDBRepo
from libs import punq


@lru_cache(1)
def get_container() -> punq.Container:
    """Singleton фабрика DI контейнера."""
    return _initialize_container()


def _initialize_container() -> punq.Container:
    """Инициализация DI контейнера."""
    container = punq.Container(reassignments_prohibited=True)

    # Config
    container.register(AWSConfig, instance=AWSConfig())
    container.register(AppConfig, instance=AppConfig())
    container.register(DatabaseConfig, instance=DatabaseConfig())

    # Resources
    container.register(DatabaseResource, factory=DatabaseResource)

    # Services
    container.register(IRandomRe, factory=RandomReXeger)  # type: ignore[misc]
    container.register(IStorage, factory=StorageS3)  # type: ignore[misc]

    # Repos
    container.register(IUploadedFileRepo, factory=UploadedFileDBRepo)  # type: ignore[misc]

    # Use Cases
    for use_case in UseCaseMeta.registered_use_cases:
        container.register(use_case)

    return container


__all__ = [
    "get_container",
]

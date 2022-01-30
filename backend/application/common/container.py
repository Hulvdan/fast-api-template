"""Dependency-injection контейнер."""
import importlib
import inspect
from functools import lru_cache
from typing import Any

from common.base import BaseUseCase
from common.config import AppConfig, AWSConfig, DatabaseConfig
from common.services.random_re import IRandomRe
from common.services.storage import IStorage
from infrastructure.database import DatabaseResource
from infrastructure.services.random_re_rstr import RandomReXeger
from infrastructure.services.storage_s3 import StorageS3
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

    _load_use_cases(container)

    return container


def _load_use_cases(container: punq.Container) -> None:
    """Загрузка всех сценариев из приложений."""
    loaded_use_cases: set[str] = set()

    apps = container.resolve(AppConfig).apps
    for app in apps:
        try:
            use_cases_module = importlib.import_module(f"domain.{app}.use_cases")
        except ModuleNotFoundError:
            continue

        module_members: list[tuple[str, Any]] = inspect.getmembers(use_cases_module)
        for member_name, member in module_members:
            member_mro = getattr(member, "mro", None)
            if member_mro is None:
                continue

            mro = member_mro()
            if len(mro) > 2 and BaseUseCase in mro:
                if member_name in loaded_use_cases:
                    continue

                loaded_use_cases.add(member_name)
                container.register(member)


__all__ = [
    "get_container",
]

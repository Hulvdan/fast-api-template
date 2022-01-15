import importlib
import inspect
from functools import lru_cache
from typing import Any

from common.services.implementations.random_re_rstr import RandomReXeger
from common.services.implementations.storage_s3 import StorageS3
from common.services.interfaces.random_re import IRandomRe
from common.services.interfaces.storage import IStorage
from core.base import BaseUseCase
from libs import punq

from .config import AppConfig, AuthConfig, AWSSettings, DatabaseConfig
from .resources import DatabaseResource


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    """Инициализация DI контейнера."""
    container = punq.Container(reassignments_prohibited=True)

    # Configs
    container.register(AppConfig, instance=AppConfig())
    container.register(AuthConfig, instance=AuthConfig())
    container.register(DatabaseConfig, instance=DatabaseConfig())
    container.register(AWSSettings, instance=AWSSettings())

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

            if BaseUseCase in member_mro():
                if member_name in loaded_use_cases:
                    continue

                loaded_use_cases.add(member_name)
                container.register(member)

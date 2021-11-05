from dependency_injector import containers, providers

from .config import AppConfig, AuthConfig, Config, DatabaseConfig, EmailConfig, StorageConfig
from .resources import Resources, StorageResource


class Container(containers.DeclarativeContainer):
    config: Config = providers.Container(Config)

    resources: Resources = providers.Container(
        Resources,
        _database_config=config.database,
        _storage_config=config.storage,
    )


resources = [
    "StorageResource",
]

configs = [
    "Config",
    "StorageConfig",
    "EmailConfig",
    "AuthConfig",
    "AppConfig",
    "DatabaseConfig",
    "StorageService",
]

__all__ = [
    "Container",
    *configs,
    *resources,
]

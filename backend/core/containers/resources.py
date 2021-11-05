from dependency_injector import containers, providers

from ..resources import DatabaseResource, StorageResource


class Resources(containers.DeclarativeContainer):
    _storage_config = providers.Dependency()
    _database_config = providers.Dependency()

    db = providers.Singleton(
        DatabaseResource,
        database_config=_database_config.provided,
    )

    storage = providers.Singleton(
        StorageResource,
        storage_config=_storage_config.provided,
    )

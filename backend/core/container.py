from libs import punq

from .config import AppConfig, AuthConfig, DatabaseConfig
from .resources import DatabaseResource


def initialize_container() -> punq.Container:
    container = punq.Container(reassignments_prohibited=True)

    container.register(AppConfig, instance=AppConfig())
    container.register(AuthConfig, instance=AuthConfig())
    container.register(DatabaseConfig, instance=DatabaseConfig())

    container.register(DatabaseResource, factory=DatabaseResource)

    return container

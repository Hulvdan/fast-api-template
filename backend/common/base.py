"""Базовые классы, необходимые для облегчённой конфигурации dependency-injection."""
from typing import Any


class UseCaseMeta(type):
    """Мета-класс сценария.

    Им удобно собирать все сценарии и регистрировать их в DI контейнер.
    """

    registered_use_cases: list[type] = []

    def __new__(mcs, *args: list[Any], **kwargs: dict[str, Any]) -> type:  # type: ignore[misc]
        """Сохраняем сценарий в список."""
        use_case_class = super().__new__(mcs, *args, **kwargs)
        UseCaseMeta.registered_use_cases.append(use_case_class)
        return use_case_class

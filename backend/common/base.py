"""Базовые классы, необходимые для облегчённой конфигурации dependency-injection."""
from typing import Any, Type


class DomainException(Exception):
    """Исключение доменной логики.

    Им удобно собирать все доменные исключения.
    """

    registered_exceptions: list[Type["DomainException"]] = []

    def __init_subclass__(cls, **kwargs: dict[str, Any]) -> None:
        """Сохраняем доменное исключение в список."""
        super().__init_subclass__(**kwargs)
        cls.registered_exceptions.append(cls)


class UseCaseMeta(type):
    """Мета-класс сценария.

    Им удобно собирать все сценарии и регистрировать их в DI контейнер.
    """

    registered_use_cases: list[type] = []

    def __new__(mcs, *args: list[Any], **kwargs: dict[str, Any]) -> type:
        """Сохраняем сценарий в список."""
        use_case_class = super().__new__(mcs, *args, **kwargs)
        UseCaseMeta.registered_use_cases.append(use_case_class)
        return use_case_class


__all__ = [
    "DomainException",
    "UseCaseMeta",
]

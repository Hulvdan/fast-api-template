"""Базовые классы, приводящие функционал домена к читаемому виду в web."""
from typing import Any, Protocol, Type

from common.base import DomainException


class _HttpException(Protocol):
    message: str
    reason: str
    status: int
    domain_exception: Type[DomainException]


class HttpExceptionMeta(type):
    """Метакласс для маппинга доменных исключений к HTTP ответам."""

    registered_exceptions: dict[Type[DomainException], Type[_HttpException]] = {}

    def __new__(mcs, name: str, bases: tuple[type, ...], dct: dict[str, Any]) -> type:
        """Сохраняем сценарий в список."""
        mcs._validate_dct(name, dct)
        http_exception_class = super().__new__(mcs, name, bases, dct)
        mcs.registered_exceptions[
            dct["domain_exception"]
        ] = http_exception_class  # type: ignore[assignment]
        return http_exception_class

    @staticmethod
    def _validate_dct(name: str, dct: dict[str, Any]) -> None:
        required_fields = {
            "message": str,
            "status": int,
            "reason": str,
            "domain_exception": DomainException,
        }
        for field, field_class in required_fields.items():
            if field_class in {int, str}:
                if not isinstance(dct[field], field_class):
                    raise ValueError(
                        "{}: '{}' is not an instance of '{}'".format(name, dct[field], field_class)
                    )
            elif field_class is DomainException:
                if not issubclass(dct[field], field_class):
                    raise ValueError(
                        "{}: '{}' is not a subclass of '{}'".format(name, dct[field], field_class)
                    )
            else:
                raise ValueError


__all__ = [
    "HttpExceptionMeta",
]

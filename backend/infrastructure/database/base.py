"""Базовый класс декларативного описания ORM моделей SQLAlchemy."""
from sqlalchemy.ext.declarative import declarative_base, declared_attr


class CustomBase:
    """Базовый класс декларативного описания ORM моделей SQLAlchemy."""

    @declared_attr
    def __tablename__(cls) -> str:  # noqa
        return cls.__name__.lower()  # type: ignore

    __mapper_args__ = {"eager_defaults": True}


Base = declarative_base(cls=CustomBase)


__all__ = [
    "Base",
]

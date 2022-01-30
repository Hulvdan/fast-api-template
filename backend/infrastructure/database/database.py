"""Подключение к базе данных с использованием SQLAlchemy."""
from contextlib import asynccontextmanager
from typing import AsyncGenerator, cast

from sqlalchemy import create_engine, orm
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy_utils import create_database, database_exists, drop_database  # type: ignore[import]

from common.config import DatabaseConfig
from common.db import Base


class DatabaseResource:
    """Подключение к базе данных с использованием SQLAlchemy."""

    def __init__(self, database_config: DatabaseConfig) -> None:
        """Создание экземпляра с сохранением конфигурации."""
        self._database_name = database_config.database
        self._database_url = database_config.database_url
        self._engine = create_async_engine(self._database_url)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(  # type: ignore
                autocommit=False, autoflush=False, bind=self._engine, class_=AsyncSession
            )
        )

    @property
    def _sync_db_url(self) -> str:
        """Костыль для использования sqlalchemy-utils. Оно не работает с асинхронным движком."""
        return self._database_url.replace("+asyncpg", "")

    def create_database(self) -> None:
        """Создание БД при условии её отсутствия.

        Следует использовать только для тестов.
        """
        if not database_exists(self._sync_db_url):
            create_database(self._sync_db_url)

    def create_tables(self) -> None:
        """Создание всех таблиц с помощью использования декларативного стиля SQLAlchemy.

        Следует использовать только для быстрого запуска интеграционных тестов.
        Это куда быстрее, чем применять миграции. Минус в том, что мы так не тестируем миграции.
        """
        engine = create_engine(self._sync_db_url)
        Base.metadata.create_all(engine)  # type: ignore
        engine.dispose()

    async def clear_tables(self) -> None:
        """Удаление записей из всех таблиц БД.

        Следует использовать только для тестов.

        На данный момент не реализовано.
        """
        raise NotImplementedError

    def drop_database(self) -> None:
        """Дроп БД при условии её наличия.

        Следует использовать только для тестов.
        """
        if database_exists(self._sync_db_url):
            drop_database(self._sync_db_url)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Получение экземпляра сессии для потока/event-loop-а."""
        session = cast(AsyncSession, self._session_factory())
        try:
            yield session
        except Exception as err:
            await session.rollback()
            raise err
        finally:
            await session.close()

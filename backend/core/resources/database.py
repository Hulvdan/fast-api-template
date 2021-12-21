import logging
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import AsyncGenerator, Callable, Generator, cast

from sqlalchemy import create_engine, orm
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy_utils import create_database, database_exists

from core.db import Base

from ..config import DatabaseConfig

logger = logging.getLogger(__name__)


class DatabaseResource:
    def __init__(self, database_config: DatabaseConfig) -> None:
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
        return self._database_url.replace("+asyncpg", "")

    async def create_database(self) -> None:
        database_url = self._sync_db_url
        if not database_exists(database_url):
            create_database(database_url)

    async def create_tables(self) -> None:
        database_url = self._sync_db_url
        engine = create_engine(database_url)
        Base.metadata.create_all(engine)  # type: ignore
        engine.dispose()

    async def clear_tables(self) -> None:
        pass

    async def drop_database(self) -> None:
        pass

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        session = cast(AsyncSession, self._session_factory())
        try:
            yield session
        except Exception as err:
            await session.rollback()
            raise err
        finally:
            await session.close()

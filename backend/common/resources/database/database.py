from contextlib import asynccontextmanager
from typing import AsyncGenerator, cast

from sqlalchemy import create_engine, orm
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy_utils import create_database, database_exists, drop_database  # type: ignore[import]

from common.config import DatabaseConfig
from common.db import Base


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

    def create_database(self) -> None:
        if not database_exists(self._sync_db_url):
            create_database(self._sync_db_url)

    def create_tables(self) -> None:
        engine = create_engine(self._sync_db_url)
        Base.metadata.create_all(engine)  # type: ignore
        engine.dispose()

    async def clear_tables(self) -> None:
        pass

    def drop_database(self) -> None:
        if database_exists(self._sync_db_url):
            drop_database(self._sync_db_url)

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

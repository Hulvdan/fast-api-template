"""Модель и репозиторий загруженных файлов на SQLAlchemy."""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID as AlchemyUUID
from sqlalchemy.ext.asyncio import AsyncSession

from domain.upload_file.repos import IUploadedFileRepo, UploadedFile
from infrastructure.database.base import Base
from infrastructure.database.database import DatabaseResource


class UploadedFileDBModel(Base):
    """SQLAlchemy модель загруженного файла."""

    url: str = Column(String)
    key: str = Column(String)
    filename: str = Column(String)
    last_modified: datetime = Column(DateTime)
    content_length: int = Column(Integer)
    upload_path: str = Column(String)
    uuid: Optional[UUID] = Column(AlchemyUUID(as_uuid=True), primary_key=True, default=uuid4)

    @classmethod
    def from_model(cls, file: UploadedFile) -> "UploadedFileDBModel":
        """Приведение из бизнес-модели."""
        return cls(
            url=file.url,
            key=file.key,
            filename=file.filename,
            last_modified=file.last_modified,
            content_length=file.content_length,
            upload_path=file.upload_path,
            uuid=file.uuid,
        )

    def to_model(self) -> UploadedFile:
        """Приведение к бизнес-модели."""
        return UploadedFile(
            url=self.url,
            key=self.key,
            filename=self.filename,
            last_modified=self.last_modified,
            content_length=self.content_length,
            upload_path=self.upload_path,
            uuid=self.uuid,
        )


class UploadedFileDBRepo(IUploadedFileRepo):
    """Репозиторий загруженных файлов, работающий с помощью SQLAlchemy."""

    def __init__(self, db_resource: DatabaseResource) -> None:
        """Пробрасываем сессию."""
        self._session = db_resource.session

    async def delete(self, uuid: UUID) -> UploadedFile:
        """Удаление конкретного файла."""

    async def create(self, file: UploadedFile) -> UploadedFile:
        """Создание файла."""
        session: AsyncSession
        async with self._session() as session:
            db_file = UploadedFileDBModel.from_model(file)
            session.add(db_file)
            await session.flush()

            file = db_file.to_model()
            await session.commit()

        return file

    async def get(self, uuid: UUID) -> Optional[UploadedFile]:
        """Получение конкретного файла."""
        session: AsyncSession
        async with self._session() as session:
            db_file = await session.get(UploadedFileDBModel, uuid)

        if db_file is None:
            return None

        return db_file.to_model()

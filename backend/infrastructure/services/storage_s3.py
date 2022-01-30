"""Реализация сервиса взаимодействия с хранилищем файлов, подобному S3 Bucket."""
from datetime import datetime
from typing import TypedDict

from aioboto3.session import Session  # type: ignore[import]

from common.config import AWSConfig
from common.services.random_re import IRandomRe
from common.services.storage import FileMeta, IAsyncFile, IStorage


class _ResponseMetadata(TypedDict):
    RequestId: str
    HostId: str
    HTTPStatusCode: int
    HTTPHeaders: dict
    RetryAttempts: int


class _ResponseHeadObject(TypedDict):
    ResponseMetadata: _ResponseMetadata
    AcceptRanges: str
    LastModified: datetime
    ContentLength: int
    ETag: str
    ContentType: str
    Metadata: dict


class StorageS3(IStorage):
    """Сервис взаимодействия с хранилищем файлов, подобному S3 Bucket."""

    def __init__(self, aws_config: AWSConfig, random_re: IRandomRe) -> None:
        """Создание экземпляра с сохранением конфигурации."""
        self.aws_config = aws_config
        self.random_re = random_re

        self.service_name = "s3"
        self.endpoint_url = self.aws_config.endpoint_url
        self.bucket = self.aws_config.storage_bucket_name
        self.aws_access_key_id = self.aws_config.access_key_id
        self.aws_secret_access_key = self.aws_config.secret_access_key

        self.session_options = {
            "aws_access_key_id": self.aws_access_key_id,
            "aws_secret_access_key": self.aws_secret_access_key,
        }
        self.client_options = {
            "service_name": self.service_name,
            "endpoint_url": self.endpoint_url,
            "aws_access_key_id": self.aws_access_key_id,
            "aws_secret_access_key": self.aws_secret_access_key,
        }
        self.resource_options = {
            "service_name": self.service_name,
            "endpoint_url": self.endpoint_url,
            "aws_access_key_id": self.aws_access_key_id,
            "aws_secret_access_key": self.aws_secret_access_key,
        }

        self.session: Session = Session(**self.session_options)

    async def upload_file(self, file: IAsyncFile, upload_path: str) -> FileMeta:
        """Загрузка файла в S3 Bucket."""
        random_str = self.random_re.execute("[a-zA-Z0-9]{60}")
        if upload_path[:-1] != "/":
            upload_path += "/"
        file_key = upload_path + random_str

        await file.seek(0)
        async with self.session.client(**self.client_options) as s3:
            await s3.upload_fileobj(file, self.bucket, file_key)
            meta: _ResponseHeadObject = await s3.head_object(Bucket=self.bucket, Key=file_key)
        file_url = self.aws_config.endpoint_url + upload_path + random_str

        return FileMeta(
            url=file_url,
            key=random_str,
            filename=file.filename,
            last_modified=meta["LastModified"],
            content_length=meta["ContentLength"],
            upload_path=upload_path,
        )

    async def delete_file(self, file_meta: FileMeta) -> None:
        """Удаление файла из S3 Bucket."""
        file_key = file_meta.upload_path + file_meta.key
        async with self.session.client(**self.client_options) as s3:
            await s3.delete_object(Bucket=self.bucket, Key=file_key)

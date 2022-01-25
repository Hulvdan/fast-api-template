"""Реализация сервиса взаимодействия с хранилищем файлов для тестов."""
from datetime import datetime

from common.config import Config
from common.services.random_re import IRandomRe
from common.services.storage import FileMeta, IAsyncFile, IStorage


class StorageMock(IStorage):
    """Мок хранилища файлов для тестов."""

    def __init__(self, config: Config, random_re: IRandomRe) -> None:
        """Создание экземпляра с сохранением конфигурации."""
        self.aws_config = config.aws
        self.random_re = random_re

    async def upload_file(self, file: IAsyncFile, upload_path: str) -> FileMeta:
        """Эмуляция загрузки файла в хранилище."""
        random_str = self.random_re.execute("[a-zA-Z0-9]{60}")
        if upload_path[:-1] != "/":
            upload_path += "/"

        file_url = self.aws_config.endpoint_url + upload_path + random_str

        return FileMeta(
            url=file_url,
            key=random_str,
            last_modified=datetime.now(),
            content_length=1,
            upload_path=upload_path,
        )

    async def delete_file(self, file_meta: FileMeta) -> None:
        """Эмуляция удаления файла в хранилище."""
        return None

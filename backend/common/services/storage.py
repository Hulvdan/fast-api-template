from abc import ABC, abstractmethod
from datetime import datetime
from typing import NamedTuple, Protocol, Union

from common.config import Config
from common.services.random_re import IRandomRe


class FileMeta(NamedTuple):
    url: str
    key: str
    last_modified: datetime
    content_length: int
    upload_path: str


class IAsyncFile(Protocol):
    async def write(self, data: Union[bytes, str]) -> None:
        ...

    async def read(self, size: int = -1) -> Union[bytes, str]:
        ...

    async def seek(self, offset: int) -> None:
        ...

    async def close(self) -> None:
        ...


class IStorage(ABC):
    @abstractmethod
    def __init__(self, config: Config, random_re: IRandomRe) -> None:
        raise NotImplementedError

    @abstractmethod
    async def upload_file(self, file: IAsyncFile, upload_path: str) -> FileMeta:
        raise NotImplementedError

    @abstractmethod
    async def delete_file(self, file_meta: FileMeta) -> None:
        raise NotImplementedError

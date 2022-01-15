from typing import Callable

from pytest import mark

from common.services.interfaces.storage import IAsyncFile
from domain.upload_file.use_cases import UploadFileUseCase
from libs.punq import Container


@mark.asyncio
@mark.domain
async def test_upload_file_use_case(
    container: Container, async_file_factory: Callable[[str], IAsyncFile]
) -> None:
    file = async_file_factory("a.png")
    response = container.resolve(UploadFileUseCase).execute(file)
    assert response

from typing import Callable

import pytest

from common.services.storage import IAsyncFile
from domain.upload_file.repos import IUploadedFileRepo
from domain.upload_file.use_cases import UploadFileUseCase
from libs.punq import Container


@pytest.mark.asyncio()
@pytest.mark.domain()
async def test_upload_file_use_case(
    container: Container,
    async_file_factory: Callable[[str], IAsyncFile],
    upload_file_repo: IUploadedFileRepo,
) -> None:
    """Проверка успешной отработки сценария загрузки файлов."""
    file = async_file_factory("a.png")
    uploaded_file = await container.resolve(UploadFileUseCase).execute(file)
    assert uploaded_file.uuid is not None

    file_from_db = await upload_file_repo.get(uploaded_file.uuid)
    assert file_from_db is not None

from typing import Callable

import pytest

from common.services.storage import IAsyncFile
from domain.upload_file.use_cases import UploadFileUseCase
from libs.punq import Container


@pytest.mark.asyncio()
@pytest.mark.domain()
async def test_upload_file_use_case(
    container: Container, async_file_factory: Callable[[str], IAsyncFile]
) -> None:
    """Проверка успешной отработки сценария загрузки файлов."""
    file = async_file_factory("a.png")
    response = container.resolve(UploadFileUseCase).execute(file)
    assert response

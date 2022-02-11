import pytest

from domain.upload_file.use_cases import DeleteFileUseCase, UploadFileUseCase


@pytest.mark.asyncio()
async def test_upload_file_use_case(container, async_file_factory, upload_file_repo) -> None:
    """Проверка успешной отработки сценария загрузки файлов."""
    file = async_file_factory("a.png")
    uploaded_file = await container.resolve(UploadFileUseCase).execute(file)
    assert uploaded_file.uuid is not None

    file_from_db = await upload_file_repo.get(uploaded_file.uuid)
    assert file_from_db is not None


@pytest.mark.asyncio()
async def test_delete_file_use_case(container, async_file_factory, upload_file_repo) -> None:
    """Проверка успешной отработки сценария удаления файлов."""
    file = async_file_factory("a.png")
    uploaded_file = await container.resolve(UploadFileUseCase).execute(file)
    assert uploaded_file.uuid is not None

    await container.resolve(DeleteFileUseCase).execute(uploaded_file.uuid)

    file_from_db = await upload_file_repo.get(uploaded_file.uuid)
    assert file_from_db is None

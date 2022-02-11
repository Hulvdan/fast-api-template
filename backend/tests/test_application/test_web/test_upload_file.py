import pytest

from domain.upload_file.repos import UploadedFile


@pytest.fixture()
async def uploaded_file(client, image_factory, upload_file_repo) -> UploadedFile:
    """Фикстура загруженного файла."""
    image = image_factory("test.png")
    files = {"image": image}
    response = await client.post("/api/v1/", files=files)
    assert response.status_code == 200

    return await upload_file_repo.get(response.json()["uuid"])


@pytest.mark.asyncio()
async def test_upload_file_view(client, image_factory) -> None:
    """Проверка endpoint-а загрузки файлов."""
    image = image_factory("test.png")
    files = {"image": image}
    response = await client.post("/api/v1/", files=files)
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["uuid"] is not None
    assert response_json["url"] is not None
    assert response_json["key"] is not None
    assert response_json["last_modified"] is not None
    assert response_json["content_length"] is not None
    assert response_json["upload_path"] is not None


@pytest.mark.asyncio()
async def test_delete_file_view_success(client, uploaded_file, upload_file_repo) -> None:
    """Проверка endpoint-а удаления файлов."""
    assert uploaded_file.uuid is not None

    response = await client.delete(f"/api/v1/{uploaded_file.uuid}")
    assert response.status_code == 204

    file_from_repo = await upload_file_repo.get(uploaded_file.uuid)
    assert file_from_repo is None


@pytest.mark.asyncio()
async def test_delete_file_view_not_found(client, upload_file_repo) -> None:
    """Проверка endpoint-а удаления файлов."""
    response = await client.delete("/api/v1/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.json()["reason"] == "file_does_not_exist"

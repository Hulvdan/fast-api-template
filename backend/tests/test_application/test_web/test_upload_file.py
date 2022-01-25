import io
from typing import Callable

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio()
@pytest.mark.web()
async def test_upload_file_view(
    client: AsyncClient, image_factory: Callable[..., io.BytesIO]
) -> None:
    """Проверка endpoint-а загрузки файлов."""
    image = image_factory("test.png")
    files = {"image": image}
    response = await client.post("/api/v1/", files=files)
    assert response.status_code == 200

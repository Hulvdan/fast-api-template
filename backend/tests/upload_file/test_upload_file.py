import io
from typing import Callable

from httpx import AsyncClient
from pytest import mark


@mark.asyncio
async def test_upload_file_view(
    client: AsyncClient, image_factory: Callable[..., io.BytesIO]
) -> None:
    image = image_factory("test.png")
    files = dict(image=image)
    response = await client.post("/api/v1/", files=files)
    assert response.status_code == 200

from pytest import mark
from starlette import status


@mark.asyncio
async def test_get_response(client):
    response = await client.get("/api/v1/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello World"}


@mark.asyncio
async def test_post(client, image_factory):
    image = image_factory("test.png")
    files = dict(image=image)
    response = await client.post("/api/v1/", files=files)
    assert response.status_code == 200

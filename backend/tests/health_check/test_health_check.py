from pytest import mark
from starlette import status


@mark.asyncio
class TestHealthCheck:
    async def test_health_check(self, client):
        response = await client.get("/api/v1/health-check", follow_redirects=True)
        assert status.HTTP_200_OK == response.status_code

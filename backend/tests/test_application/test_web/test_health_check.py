import pytest
from starlette import status


@pytest.mark.asyncio()
class TestHealthCheck:
    async def test_health_check(self, client) -> None:
        """Проверка работы health check-а."""
        response = await client.get("/api/v1/health-check", follow_redirects=True)
        assert status.HTTP_200_OK == response.status_code

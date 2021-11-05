from datetime import datetime, timedelta

import jwt
from pytest import fixture, mark
from starlette import status

from core.containers.config import AuthConfig


@mark.asyncio
class VerifyTokenTestCase:
    @fixture(autouse=True)
    async def setup(self):
        self.token_good = await self.generate_jwt(
            datetime.utcnow() + timedelta(minutes=30), AuthConfig.secret_key
        )
        self.token_expired = await self.generate_jwt(
            datetime.utcnow() - timedelta(minutes=30), AuthConfig.secret_key
        )
        self.token_with_other_sign = await self.generate_jwt(
            datetime.utcnow(), "Im not secret key :)"
        )

    @staticmethod
    async def generate_jwt(exp_time: datetime, secret: str) -> str:
        return jwt.encode({"message": "hello world", "exp": exp_time}, secret)

    async def test_with_good_token(self, client):
        token = self.token_good

        response = await client.post(
            "api/v1/verify-token",
            headers={"Authorization": "{} {}".format(AuthConfig.jwt_auth_header_prefix, token)},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"token": token}

    async def test_with_token_expired(self, client):
        token = self.token_expired

        response = await client.post(
            "api/v1/verify-token",
            headers={"Authorization": "{} {}".format(AuthConfig.jwt_auth_header_prefix, token)},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_with_with_other_sign(self, client):
        token = self.token_with_other_sign

        response = await client.post(
            "api/v1/verify-token",
            headers={"Authorization": "{} {}".format(AuthConfig.jwt_auth_header_prefix, token)},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_no_authentication_header(self, client, session):
        self.assertIsNotNone(session)
        response = await client.post("api/v1/verify-token")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

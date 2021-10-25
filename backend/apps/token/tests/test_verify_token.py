from datetime import datetime, timedelta

import jwt
from pytest import mark
from starlette import status

from core import config
from core.tests.transaction_test_case import TransactionTestCase


@mark.asyncio
class VerifyTokenTestCase(TransactionTestCase):
    async def setUp(self):
        self.token_good = await self.generate_jwt(
            datetime.utcnow() + timedelta(minutes=30), config.SECRET_KEY
        )
        self.token_expired = await self.generate_jwt(
            datetime.utcnow() - timedelta(minutes=30), config.SECRET_KEY
        )
        self.token_with_other_sign = await self.generate_jwt(
            datetime.utcnow(), "Im not secret key :)"
        )

    @staticmethod
    async def generate_jwt(exp_time: datetime, secret: str) -> str:
        return jwt.encode({"message": "hello world", "exp": exp_time}, secret)

    async def test_with_good_token(self):
        token = self.token_good

        response = self.client.post(
            "api/v1/verify-token",
            headers={"Authorization": "{} {}".format(config.JWT_AUTH_HEADER_PREFIX, token)},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"token": token})

    async def test_with_token_expired(self):
        token = self.token_expired

        response = self.client.post(
            "api/v1/verify-token",
            headers={"Authorization": "{} {}".format(config.JWT_AUTH_HEADER_PREFIX, token)},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    async def test_with_with_other_sign(self):
        token = self.token_with_other_sign

        response = self.client.post(
            "api/v1/verify-token",
            headers={"Authorization": "{} {}".format(config.JWT_AUTH_HEADER_PREFIX, token)},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    async def test_no_authentication_header(self):
        self.assertIsNotNone(self.session)
        response = self.client.post("api/v1/verify-token")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

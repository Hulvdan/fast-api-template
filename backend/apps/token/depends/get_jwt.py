import re

from dependency_injector.wiring import Provide
from fastapi import Header, HTTPException
from starlette import status
from starlette.requests import Request

from apps.token.constants.jwt import JWT_REGEX
from core.containers import Container


def get_jwt(
    request: Request,
    authorization: str = Header("", alias="Authorization"),
    auth_config=Provide[Container.config.auth],
) -> str:
    regex = JWT_REGEX.format(auth_config.jwt_auth_header_prefix)

    if not re.match(regex, authorization):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization has wrong format",
        )

    return authorization.split(" ")[-1]

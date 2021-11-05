import jwt
from dependency_injector.wiring import Provide
from fastapi import Depends, HTTPException
from starlette import status
from starlette.requests import Request

from apps.token.depends.get_jwt import get_jwt
from core.containers import Container
from core.containers.config import AuthConfig


def get_token_decoded(
    request: Request,
    jwt_token: str = Depends(get_jwt),
    auth_config: AuthConfig = Provide[Container.config.auth],
) -> str:
    try:
        token = jwt.decode(jwt_token, auth_config.jwt_secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
    except jwt.InvalidSignatureError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))

    return token

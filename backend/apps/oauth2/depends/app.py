from dependency_injector.wiring import Provide, inject
from fastapi import Header
from sqlalchemy import String, cast, select
from sqlalchemy.dialects.postgresql import ARRAY

from apps.oauth2.models import AccessToken, App
from core.containers import Container
from core.utils.get_object_or_404 import get_object_or_404


def get_app_object_scopes(scopes):
    @inject
    async def wrapper(
        db=Provide[Container.resources.db],
        authorization: str = Header(..., alias="Authorization"),
    ):
        async with db.session() as session:
            _, authorization_splited = authorization.split(" ")
            obj = get_object_or_404(
                await session.execute(
                    select(App)
                    .join(AccessToken)
                    .filter(
                        AccessToken.access_token == authorization_splited,
                        AccessToken.scopes.contains(cast(scopes, ARRAY(String))),
                    )
                )
            )
        return obj

    return wrapper

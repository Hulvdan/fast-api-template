from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import raiseload, subqueryload
from starlette import status

from core.containers import Container
from core.resources.database import DatabaseResource
from core.utils.get_object_or_404 import get_object_or_404

from ..models.access_token import AccessToken
from ..models.apps import App
from ..serializers.token_access import TokenAccess, TokenOut

router = APIRouter()


@router.post("/token", response_model=TokenOut)
@inject
async def login_for_access_token(
    access: TokenAccess = Depends(),
    db: DatabaseResource = Depends(Provide[Container.resources.db]),
    auth_config=Depends(Provide[Container.config.auth]),
):
    async with db.session() as session:
        statement = (
            select(App)
            .filter(App.client_secret == access.client_secret, App.client_id == access.client_id)
            .options(subqueryload(App.access_tokens), raiseload("*"))
        )
        app = get_object_or_404(await session.execute(statement))
        scopes = access.scopes

        if len(scopes) == 0:
            scopes = [list(auth_config.oauth_scopes.keys())[0]]

        allowed_scopes = auth_config.oauth_scopes.keys()

        for scope in scopes:
            if scope not in allowed_scopes:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"scope": f"{scope} scope is not in allowed scopes"},
                )

        access_token = AccessToken(scopes=scopes)
        session.add(access_token)
        await session.commit()
        await session.refresh(access_token)
        await session.refresh(app)
        app.access_tokens.append(access_token)
        await session.commit()
        await session.refresh(access_token)

    return {"access_token": access_token.access_token, "token_type": "bearer"}

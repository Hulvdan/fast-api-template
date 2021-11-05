from dataclasses import dataclass

from pytest import fixture, mark
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import raiseload, subqueryload
from starlette import status

from apps.oauth2.models import AccessToken, App


@dataclass
class _Tokens:
    access_token_bad: AccessToken
    access_token_good: AccessToken
    access_token_superset: AccessToken
    access_token_none: AccessToken


@fixture
async def tokens(session: AsyncSession) -> _Tokens:
    app_model = App(name="App test")

    session.add(app_model)
    await session.commit()
    await session.refresh(app_model)
    client_id = app_model.client_id
    client_secret = app_model.client_secret

    access_token_good = AccessToken(scopes=["me"])
    access_token_bad = AccessToken(scopes=["em"])
    access_token_superset = AccessToken(scopes=["me", "em"])
    access_token_none = AccessToken(scopes=[])

    session.add(access_token_good)
    session.add(access_token_bad)
    session.add(access_token_superset)
    session.add(access_token_none)

    statement = (
        select(App)
        .filter(App.client_id == client_id, App.client_secret == client_secret)
        .options(subqueryload(App.access_tokens), raiseload("*"))
    )
    app_model = (await session.execute(statement)).scalar_one()
    app_model.access_tokens.append(access_token_bad)
    app_model.access_tokens.append(access_token_good)
    app_model.access_tokens.append(access_token_superset)
    app_model.access_tokens.append(access_token_none)
    await session.commit()

    await session.refresh(access_token_bad)
    await session.refresh(access_token_good)
    await session.refresh(access_token_superset)
    await session.refresh(access_token_none)

    return _Tokens(
        access_token_bad=access_token_bad,
        access_token_good=access_token_good,
        access_token_superset=access_token_superset,
        access_token_none=access_token_none,
    )


@mark.asyncio
async def test_get_app_good_scopes(client, tokens):
    headers = {"Authorization": f"bearer {tokens.access_token_good.access_token}"}

    response = await client.get("api/v1/me", headers=headers)

    assert response.status_code == status.HTTP_200_OK

    payload = response.json()

    assert "name" in payload
    assert "created" in payload
    assert "modified" in payload


@mark.asyncio
async def test_get_app_good_scopes_superset(client, tokens):
    headers = {"Authorization": f"bearer {tokens.access_token_superset.access_token}"}

    response = await client.get("api/v1/me", headers=headers)

    assert response.status_code == status.HTTP_200_OK

    payload = response.json()

    assert "name" in payload
    assert "created" in payload
    assert "modified" in payload


@mark.asyncio
async def test_get_app_good_scopes_none(client, tokens):
    headers = {"Authorization": f"bearer {tokens.access_token_none.access_token}"}

    response = await client.get("api/v1/me", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@mark.asyncio
async def test_get_app_bad_scopes(client, tokens):
    headers = {"Authorization": f"bearer {tokens.access_token_bad.access_token}"}

    response = await client.get("api/v1/me", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@mark.asyncio
async def test_get_app_bad_auth(client, tokens):
    headers = {"Authorization": f"bearer ffffffffffffffffffffffffffffffff"}

    response = await client.get("api/v1/me", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND

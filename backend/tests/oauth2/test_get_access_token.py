from pytest import fixture, mark
from sqlalchemy import select
from starlette import status

from apps.oauth2.models import AccessToken, App
from core.utils.get_object_or_404 import get_object


@fixture
async def app_model(session):
    app_model = App(name="App test")
    session.add(app_model)
    await session.commit()

    await session.refresh(app_model)

    yield app_model


@mark.asyncio
async def test_send_json(client, app_model):
    data = {
        "client_id": app_model.client_id,
        "client_secret": app_model.client_secret,
        "grant_type": "client_credentials",
    }

    headers = {"Content-Type": "application/json"}

    response = await client.post("api/v1/token", data=data, headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@mark.asyncio
async def test_send_form(client, session, app_model):
    data = {
        "client_id": app_model.client_id,
        "client_secret": app_model.client_secret,
        "grant_type": "client_credentials",
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = await client.post("api/v1/token", data=data, headers=headers)

    assert response.status_code == status.HTTP_200_OK

    payload = response.json()

    access_token = get_object(
        await session.execute(
            select(AccessToken).filter(AccessToken.access_token == payload.get("access_token"))
        )
    )

    assert access_token is not None
    assert {"access_token": str(access_token.access_token), "token_type": "bearer"} == payload


@mark.asyncio
async def test_send_bad_grant_type(client, app_model):
    data = {
        "client_id": app_model.client_id,
        "client_secret": app_model.client_secret,
        "grant_type": "client_credentialss",
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = await client.post("api/v1/token", data=data, headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@mark.asyncio
async def test_send_not_exist_app(client, app_model):
    data = {
        "client_id": f"{str(app_model.client_id)[:-1]}a",
        "client_secret": str(app_model.client_secret),
        "grant_type": "client_credentials",
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = await client.post("api/v1/token", data=data, headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND

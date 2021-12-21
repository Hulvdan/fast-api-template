from http import HTTPStatus
from typing import Any

from fastapi import File, UploadFile
from fastapi.routing import APIRouter

router = APIRouter()


# @router.get("/")
# async def hello_world():
#     return {"message": "Hello World"}


@router.post("/", status_code=HTTPStatus.OK)
async def hello_world(image: UploadFile = File(...)) -> Any:
    return {}

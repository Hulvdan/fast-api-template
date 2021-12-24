from http import HTTPStatus
from typing import Any

from fastapi import Depends, File, UploadFile
from fastapi.routing import APIRouter

from core.container import get_container
from libs.punq import Container

from . import models, use_cases

router = APIRouter()


@router.get("/", status_code=HTTPStatus.OK)
async def get_hello_world() -> Any:
    return dict(message="Hello World")


@router.post("/", status_code=HTTPStatus.OK, response_model=models.PostHelloWorldResponse)
async def post_hello_world(
    image: UploadFile = File(...), container: Container = Depends(get_container)
) -> Any:
    file_meta = await container.resolve(use_cases.HelloWorldUseCase).execute(image)
    return dict(
        url=file_meta.url,
        filename=file_meta.filename,
        key=file_meta.key,
        content_type=file_meta.content_type,
        last_modified=file_meta.last_modified,
        content_length=file_meta.content_length,
        upload_path=file_meta.upload_path,
    )

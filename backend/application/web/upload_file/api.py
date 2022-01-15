from http import HTTPStatus
from typing import Any

from fastapi import Depends, File, UploadFile
from fastapi.routing import APIRouter

from common.container import get_container
from domain.upload_file import models, use_cases
from libs.punq import Container

router = APIRouter()


@router.post("/", status_code=HTTPStatus.OK, response_model=models.UploadFileResponse)
async def upload_file(
    image: UploadFile = File(...), container: Container = Depends(get_container)
) -> Any:
    file_meta = await container.resolve(use_cases.UploadFileUseCase).execute(image)
    return dict(
        url=file_meta.url,
        filename=file_meta.filename,
        key=file_meta.key,
        content_type=file_meta.content_type,
        last_modified=file_meta.last_modified,
        content_length=file_meta.content_length,
        upload_path=file_meta.upload_path,
    )

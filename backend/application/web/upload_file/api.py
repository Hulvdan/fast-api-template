from http import HTTPStatus

from fastapi import Depends, File, UploadFile
from fastapi.routing import APIRouter

from common.container import get_container
from domain.upload_file import use_cases
from libs.punq import Container

from . import models

router = APIRouter()


@router.post("/", status_code=HTTPStatus.OK, response_model=models.UploadFileResponse)
async def upload_file(
    image: UploadFile = File(...), container: Container = Depends(get_container)  # noqa: B008
) -> models.UploadFileResponse:
    file_meta = await container.resolve(use_cases.UploadFileUseCase).execute(image)
    return models.UploadFileResponse.parse_obj(
        {
            "url": file_meta.url,
            "key": file_meta.key,
            "last_modified": file_meta.last_modified,
            "content_length": file_meta.content_length,
            "upload_path": file_meta.upload_path,
        }
    )

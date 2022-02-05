"""API приложения загрузки файлов."""
from http import HTTPStatus

from fastapi import Depends, File, UploadFile
from fastapi.routing import APIRouter

from application.common.container import get_container
from domain.upload_file import use_cases
from libs.punq import Container

from . import models

router = APIRouter()


@router.post("/", status_code=HTTPStatus.OK, response_model=models.UploadFileResponse)
async def upload_file(
    image: UploadFile = File(...), container: Container = Depends(get_container)  # noqa: B008
) -> models.UploadFileResponse:
    """Endpoint загрузки файла."""
    uploaded_file = await container.resolve(use_cases.UploadFileUseCase).execute(image)
    return models.UploadFileResponse.parse_obj(
        {
            "uuid": uploaded_file.uuid,
            "url": uploaded_file.url,
            "key": uploaded_file.key,
            "last_modified": uploaded_file.last_modified,
            "content_length": uploaded_file.content_length,
            "upload_path": uploaded_file.upload_path,
        }
    )

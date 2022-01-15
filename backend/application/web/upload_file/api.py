from http import HTTPStatus

from fastapi import Depends, File, UploadFile
from fastapi.routing import APIRouter

from common.container import get_container
from domain.upload_file import models, use_cases
from libs.punq import Container

router = APIRouter()


@router.post("/", status_code=HTTPStatus.OK, response_model=models.UploadFileResponse)
async def upload_file(
    image: UploadFile = File(...), container: Container = Depends(get_container)
) -> models.UploadFileResponse:
    return await container.resolve(use_cases.UploadFileUseCase).execute(image)

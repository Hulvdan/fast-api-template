from http import HTTPStatus

from dependency_injector.wiring import Provide
from fastapi import Depends, File, UploadFile
from fastapi.routing import APIRouter

from core.containers import Container
from core.resources import StorageResource

router = APIRouter()


@router.get("/")
async def hello_world():
    return {"message": "Hello World"}


@router.post("/", status_code=HTTPStatus.OK)
async def hello_world(
    image: UploadFile = File(...),
    storage_resource: StorageResource = Depends(Provide[Container.resources.storage]),
):
    return {}

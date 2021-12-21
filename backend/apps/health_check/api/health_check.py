from typing import Any

from fastapi.routing import APIRouter
from starlette import status
from starlette.responses import Response

router = APIRouter()


@router.get("/")
def health_check() -> Any:
    return Response(status_code=status.HTTP_200_OK)

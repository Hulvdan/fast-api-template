"""Обычный health check."""
from typing import Any

from fastapi.routing import APIRouter
from starlette import status
from starlette.responses import Response

router = APIRouter()


@router.get("/health-check")
def health_check() -> Any:
    """Обычный health check."""
    return Response(status_code=status.HTTP_200_OK)

from fastapi.routing import APIRouter

from .health_check.api import router as router_health_check
from .upload_file.api import router as router_upload_file

router = APIRouter()
router.include_router(router_health_check, prefix="/api/v1", tags=["health_check"])
router.include_router(router_upload_file, prefix="/api/v1", tags=["hello_world"])

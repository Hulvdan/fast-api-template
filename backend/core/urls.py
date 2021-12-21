from fastapi.routing import APIRouter

from apps.health_check.urls import router as router_health_check
from apps.hello_world.urls import router as router_hello_world

router = APIRouter()
router.include_router(router_health_check, prefix="/api/v1", tags=["health_check"])
router.include_router(router_hello_world, prefix="/api/v1", tags=["hello_work"])

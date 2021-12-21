from fastapi.routing import APIRouter

from apps.hello_world.api.hello_world import router as routes

router = APIRouter()

router.include_router(routes)

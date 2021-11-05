from typing import Any

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from ..depends import get_app_object_scopes
from ..models import App
from ..serializers.app import AppOut

router = APIRouter()


@router.get("/me", response_model=AppOut)
def me(app: App = Depends(get_app_object_scopes(["me"]))) -> Any:
    return jsonable_encoder(app)

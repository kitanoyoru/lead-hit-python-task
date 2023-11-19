import logging
from typing import Any, AsyncGenerator, Callable

from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from src.service import Service

gger = logging.getLogger(__name__)


def create_router(
    get_service: Callable[[], AsyncGenerator[Service, Any]],
) -> APIRouter:
    router = APIRouter()

    @router.get(
        "/get_form",
        name="Get form",
        description="Get form according to the specified query",
        response_class=ORJSONResponse,
    )
    async def get_form(service: Service = Depends(get_service), **params):
        try:
            return await service.search_form_template(params)
        except ValueError:
            ...
        except NotFound:
            ...

    return router

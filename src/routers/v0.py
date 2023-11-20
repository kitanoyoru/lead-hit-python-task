import logging

from typing import Any, AsyncGenerator, Callable

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import ORJSONResponse

from src.errors import NotFoundException, ValidatorException
from src.service import Service

logger = logging.getLogger(__name__)


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
    async def get_form(request: Request, service: Service = Depends(get_service)):
        params = dict(request.query_params)

        try:
            return await service.search_form_template(**params)
        except ValidatorException as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
            )
        except NotFoundException as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

    return router

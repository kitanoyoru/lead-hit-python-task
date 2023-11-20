from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Response
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request as StarletteRequest

from src.config import create_client_from_env, get_database_from_env
from src.routers.v0 import create_router as create_api_router
from src.service import Service


class CustomCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: StarletteRequest, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response


def create_app() -> FastAPI:
    client = create_client_from_env()

    return create_app_with_config(
        client=client,
    )


def create_app_with_config(client: AsyncIOMotorClient[Any]) -> FastAPI:
    app = FastAPI(
        title="Leadhit task",
        version="0.1.0",
        description="",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "displayRequestDuration": 1,
        },
    )
    app.add_middleware(CustomCORSMiddleware)

    async def get_service():
        db = get_database_from_env(client)
        service = Service(db)
        yield service

    api_router = create_api_router(get_service)
    app.include_router(api_router, prefix="/api/v0", tags=["api", "v0"])

    return app

from __future__ import annotations

from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request as StarletteRequest

from src.config import create_client_from_env, get_database_from_env, get_directories
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


def create_app_with_config(client: AsyncIOMotorClient) -> FastAPI:
    directories = get_directories()

    app = FastAPI(
        title="",
        version="0.1.0",
        description="",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "displayRequestDuration": 1,
        },
    )
    app.add_middleware(CustomCORSMiddleware)

    app.mount(
        "/static",
        StaticFiles(directory=directories.static),
        name="static",
    )

    async def get_service():
        async with client.start_session(causal_consistency=True) as session:
            async with session.start_transaction():
                db = get_database_from_env(client)
                service = Service.with_session(db, session)
                yield service

    api_router = create_api_router(get_service)
    app.include_router(api_router, prefix="/api/v0", tags=["api", "v0"])

    return app

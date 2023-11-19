import os
import pathlib
from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorClient


@dataclass
class Directories:
    static: str
    templates: str
    test_data: str


def get_directories() -> Directories:
    root_dir = pathlib.Path(__file__).parent

    return Directories(
        static=str(root_dir / "static"),
        templates=str(root_dir / "templates"),
        test_data=str(root_dir / "test_data"),
    )


def get_database_url() -> str:
    return f"mongod+srv://{os.environ['DATABASE_URL']}"


def get_database_from_env(client: AsyncIOMotorClient) -> str:
    return client[os.getenv("DB_NAME")]


def create_client_from_env() -> AsyncIOMotorClient:
    MONGODB_DATABASE_URL = f"mongod+srv://{os.environ['DATABASE_URL']}"

    client = AsyncIOMotorClient(MONGODB_DATABASE_URL)

    return client

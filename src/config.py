import os
import pathlib
from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


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


def get_database_from_env(client: AsyncIOMotorClient) -> AsyncIOMotorDatabase:
    db_name = os.getenv("DATABASE_NAME")
    if db_name is None:
        raise RuntimeError("Please set up DATABASE_NAME env variable")

    return client[db_name]


def create_client_from_env() -> AsyncIOMotorClient:
    MONGODB_DATABASE_URL = f"mongodb://{os.environ['DATABASE_URL']}"
    client = AsyncIOMotorClient(MONGODB_DATABASE_URL)
    return client

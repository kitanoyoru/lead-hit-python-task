from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorDatabase

from src.database import Database
from src.models import create_form_template_model


class Service:
    def __init__(
        self,
        db: AsyncIOMotorDatabase,
        session: Optional[AsyncIOMotorClientSession] = None,
    ):
        self._db = Database(db, session)

    async def search_form_template(self, **fields):
        if (
            template := await self._db.search_form_template(field_names=fields.keys())
        ) is not None:
            Model = create_form_template_model("SomeModel", raw_data=template)
            m = Model(**fields)
            return m.__class__.__name__

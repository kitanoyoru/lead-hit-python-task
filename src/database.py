from typing import Optional, Sequence

from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorDatabase


class Database:
    _FORM_TEMPLATE_COLLECTION = "form_template_collection"

    def __init__(
        self,
        db: AsyncIOMotorDatabase,
        session: Optional[AsyncIOMotorClientSession] = None,
    ):
        self._db = db
        self._db_options = {
            "session": session,
        }

    async def search_form_template(self, field_names: Sequence[str]):
        options = {name: {"$exists": True} for name in field_names}

        if (
            template := await self._db[self._FORM_TEMPLATE_COLLECTION].find_one(
                options, projection={"_id": 0}, **self._db_options
            )
        ) is not None:
            return template

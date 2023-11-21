from typing import Any, Dict, KeysView, Optional, Union

from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorDatabase

from src.errors import NotFoundException

# fix
DatabaseOption = Union[AsyncIOMotorClientSession, None]


class Database:
    _FORM_TEMPLATE_COLLECTION: str = "formTemplateCollection"

    def __init__(
        self,
        db: AsyncIOMotorDatabase,
        session: Optional[AsyncIOMotorClientSession] = None,
    ):
        self._db = db
        self._db_options: Dict[str, DatabaseOption] = {
            "session": session,
        }

    async def search_form_template(self, field_names: KeysView[str]) -> Dict[str, Any]:
        options: Dict[str, Dict[str, bool]] = {
            name: {"$exists": True} for name in field_names
        }

        if (
            template := await self._db[self._FORM_TEMPLATE_COLLECTION].find_one(
                options, projection={"_id": 0}, **self._db_options
            )
        ) is not None:
            return template

        raise NotFoundException()

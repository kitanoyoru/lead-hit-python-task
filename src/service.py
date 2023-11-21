from typing import Dict, Optional

from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorDatabase

from src.database import Database
from src.errors import ValidatorException
from src.models import create_form_template_model, validators


class Service:
    def __init__(
        self,
        db: AsyncIOMotorDatabase,
        session: Optional[AsyncIOMotorClientSession] = None,
    ):
        self._db = Database(db, session)

    async def search_form_template(self, fields: Dict[str, str]) -> Optional[str]:
        template = await self._db.search_form_template(field_names=fields.keys())
        name = template.pop("name")

        Model = create_form_template_model(name, raw_data=template)
        m = Model(**fields)

        return m.__class__.__name__

    def validate_fields(self, fields: Dict[str, str]) -> Dict[str, str]:
        field_types: Dict[str, str] = {}

        for field_name, value in fields.items():
            for field_type, validator in validators.items():
                try:
                    validator(value)
                    field_types[field_name] = field_type.value
                    break
                except ValidatorException:
                    continue

        return field_types

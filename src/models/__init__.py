import re
from collections import OrderedDict
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, Optional, Type

from pydantic import BaseModel, create_model, field_validator


def _email_validator(value: Any):
    assert isinstance(value, str), "value should be str"

    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    assert re.match(pattern, value), "invalid email formay"

    return value


def _phone_validator(value: Any) -> str:
    assert isinstance(value, str), "value should be str"

    cleaned_number = re.sub(r"\D", "", value)
    assert re.match(
        r"^7\d{9}$", cleaned_number
    ), "invalid phone format (expected format: +7 xxx xxx xx xx)"

    return value


def _date_validator(value: Any) -> str:
    assert isinstance(value, str), "value should be str"

    date: Optional[datetime] = None

    date_formats = ["%d.%m.%Y", "%Y-%m-%d"]
    for date_format in date_formats:
        try:
            date = datetime.strptime(value, date_format)
        except ValueError:
            continue

    assert date is not None

    return value


def _text_validator(value: Any) -> str:
    assert isinstance(value, str), "value should be str"

    assert len(value) < 50, "text exceeds the maximum length of 50 characters"

    return value


class FieldType(Enum):
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    DATE = "DATE"
    TEXT = "TEXT"


validators: Dict[FieldType, Callable[[Any], str]] = OrderedDict(
    {
        FieldType.EMAIL: _email_validator,
        FieldType.PHONE: _phone_validator,
        FieldType.DATE: _date_validator,
        FieldType.TEXT: _text_validator,
    }
)


def _create_validators(
    form_template: Dict[str, str]
) -> Dict[str, Callable[[Any], Any]]:
    validators: Dict[str, Callable[[Any], Any]] = {}

    for field_name, field_type in form_template.items():
        validator_name = f"{field_name}_validator"
        validator = validators[FieldType(field_type)]

        validator = field_validator(field_name)(validator)

        validators[validator_name] = validator

    return validators


def create_form_template_model(
    form_name: str, raw_data: Dict[str, Any]
) -> Type[BaseModel]:
    validators = _create_validators(raw_data)
    Model = create_model(
        form_name,
        __validators__=validators,
        **{field_name: (Optional[Any], ...) for field_name in raw_data.keys()},
    )
    return Model

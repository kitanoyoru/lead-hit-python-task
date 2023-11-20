import re
from collections import OrderedDict
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, Optional

from pydantic import create_model, field_validator

from src.errors import ValidatorException


def _email_validator(value: Any):
    if not isinstance(value, str):
        raise ValidatorException("Invalid email format")

    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if not re.match(pattern, value):
        raise ValidatorException("Invalid email format")

    return value


def _phone_validator(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("Invalid phone format")

    cleaned_number = re.sub(r"\D", "", value)

    if not re.match(r"^7\d{9}$", cleaned_number):
        raise ValidatorException(
            "Invalid phone format. Expected format: +7 xxx xxx xx xx"
        )

    return value


def _date_validator(value) -> str:
    if not isinstance(value, str):
        raise ValidatorException("Invalid date format")

    try:
        date_formats = ["%d.%m.%Y", "%Y-%m-%d"]
        for date_format in date_formats:
            datetime.strptime(value, date_format)
            return

        raise ValueError("Invalid date format")
    except ValueError:
        raise ValidatorException("Invalid date format")

    return value


def _text_validator(value: Any) -> str:
    if not isinstance(value, str):
        raise ValidatorException("Invalid text format")

    if len(value) > 50:
        raise ValidatorException("Text exceeds the maximum length of 50 characters")

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


def get_validator_for_type(field_type: str):
    return validators[FieldType(field_type)]


def create_validators(form_template: Dict[str, str]):
    validators = {}

    for field_name, field_type in form_template.items():
        validator_name = f"{field_name}_validator"
        validator = get_validator_for_type(FieldType(field_type))

        validator = field_validator(field_name)(validator)

        validators[validator_name] = validator

    return validators


def create_form_template_model(form_name: str, raw_data: Dict[str, Any]):
    validators = create_validators(raw_data)
    Model = create_model(
        form_name,
        **{field_name: (Optional[Any], None) for field_name in raw_data.keys()},
        __validators__=validators,
    )
    return Model

import re
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict

from pydantic import create_model, field_validator


def email_validator(value: Any):
    if not isinstance(value, str):
        raise ValueError("Invalid email format")

    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if not re.match(pattern, value):
        raise ValueError("Invalid email format")

    return value


def phone_validator(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("Invalid phone format")

    cleaned_number = re.sub(r"\D", "", value)

    if not re.match(r"^7\d{9}$", cleaned_number):
        raise ValueError("Invalid phone format. Expected format: +7 xxx xxx xx xx")

    return value


def date_validator(value) -> str:
    if not isinstance(value, str):
        raise ValueError("Invalid date format")

    try:
        date_formats = ["%d.%m.%Y", "%Y-%m-%d"]
        for date_format in date_formats:
            datetime.datetime.strptime(value, date_format)
            return

        raise ValueError("Invalid date format")
    except ValueError:
        raise ValueError("Invalid date format")

    return value


def text_validator(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("Invalid text format")

    if len(value) > 50:
        raise ValueError("Text exceeds the maximum length of 50 characters")

    return value


class FieldType(Enum):
    EMAIL = "email"
    PHONE = "phone"
    DATE = "date"
    TEXT = "text"

    _validators: Dict["FieldType", Callable[[Any], str]] = {
        EMAIL: email_validator,
        PHONE: phone_validator,
        DATE: date_validator,
        TEXT: text_validator,
    }

    @classmethod
    def get_validator_for_type(cls, field_type: str):
        return cls._validators[field_type]


def create_validators(form_template: Dict[str, str]):
    validators = {}

    for field_name, field_type in form_template.items():
        validator_name = f"{field_name}_validator"
        validator = field_validator(field_name, FieldType.get_validator_for(field_type))

        validators[validator_name] = validator

    return validators


def create_form_template_model(form_name: str, raw_data: Dict[str, Any]):
    validators = create_validators(raw_data)
    Model = create_model(
        form_name,
        **{field_name: (Any, ...) for field_name in raw_data.keys()},
        __validators__=validators,
    )
    return Model

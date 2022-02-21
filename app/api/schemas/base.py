from datetime import datetime, date

from pydantic import BaseModel, Field


class Id(BaseModel):
    id: int


class Timestamp(int):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if isinstance(value, datetime):
            return int(value.timestamp())
        if isinstance(value, date):
            return int(
                datetime.fromisoformat(value.isoformat()).timestamp())
        if isinstance(value, float):
            return int(value)
        else:
            return value


def TextField(*args, **kwargs):
    return Field(*args, **{'max_length': 255, **kwargs})

from typing import Annotated

from pydantic import BaseModel, Field


class Message(BaseModel):
    message: Annotated[str, Field(description='Message body')]

    @classmethod
    def Ok(cls):
        return cls(message='ok')

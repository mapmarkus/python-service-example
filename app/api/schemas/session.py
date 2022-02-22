from sqlite3 import Timestamp
from typing import Annotated
# from uuid import uuid4

from pydantic import UUID4, BaseModel, Field, Json


class Session(BaseModel):
    # id: Annotated[UUID4, Field(default_factory=uuid4)]
    id: Annotated[UUID4, Field(description='Session ID')]
    data: Json
    created_at: Timestamp
    expires_at: Timestamp

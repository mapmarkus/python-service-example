from typing import Annotated, Any, Dict
from app.api.schemas.base import Timestamp

from pydantic import UUID4, BaseModel, Field


class SessionBody(BaseModel):
    id: Annotated[UUID4, Field(description='Session ID')]
    data: Dict[str, Any]


class Session(SessionBody):
    created_at: Timestamp
    expires_at: Timestamp

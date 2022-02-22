from fastapi import APIRouter, HTTPException
from pydantic import UUID4
from app.api.schemas.session import Session

from app.store import store

router = APIRouter()


@router.get('/{id}', response_model=Session)
async def get_session(id: UUID4):
    if await store.exists(id):
        return Session(**await store.get_item_json(id))
    else:
        raise HTTPException(status_code=404)

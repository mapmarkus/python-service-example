from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from pydantic import UUID4

from app.api.schemas.session import Session, SessionBody
from app.constants import STORE_KEY, SESSION_MAX_AGE

from app.store import store

router = APIRouter()


@router.get('/{id}', response_model=Session)
async def get_session(id: UUID4):
    if await store.exists(STORE_KEY.format(session_id=id)):
        return await store.get_json(STORE_KEY.format(session_id=id))
    else:
        raise HTTPException(status_code=404)


@router.post('/', response_model=Session)
async def post_session(body: SessionBody):
    if await store.exists(STORE_KEY.format(session_id=id)):
        raise HTTPException(status_code=409)
    else:
        timestamps = dict(
            created_at=datetime.now(),
            expires_at=datetime.now() + SESSION_MAX_AGE
        )
        session = {**body.dict(), **timestamps}
        await store.set_json(STORE_KEY.format(session_id=body.id), session, until=timestamps['expires_at'])
        return session

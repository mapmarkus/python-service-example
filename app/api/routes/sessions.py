from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def get_sessions_list():
    return []
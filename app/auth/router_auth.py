from fastapi import APIRouter
from .schemas import AuthDetails

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/register')
async def register(auth_details: AuthDetails) -> dict:
    return {}

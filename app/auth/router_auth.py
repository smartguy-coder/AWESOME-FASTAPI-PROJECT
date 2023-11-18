from fastapi import APIRouter, status
from .schemas import AuthDetails, AuthRegistered

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(auth_details: AuthDetails) -> AuthRegistered:
    return {}

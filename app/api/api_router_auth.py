from fastapi import APIRouter, Depends, Header, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth_lib import AuthHandler
from app.auth.security_lib import SecurityHandler
from app.database import get_async_session
from app.schemas.schemas_user import LoginResponse, UserResponse

auth_protected_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
    dependencies=[Depends(SecurityHandler.oauth2_scheme), Depends(SecurityHandler.get_current_user)],
)

guest_router = APIRouter(
    prefix="/api/auth",
    tags=["API", "Auth"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@guest_router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def user_login(data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    result = await AuthHandler.get_login_token(data, session)
    return result


@guest_router.post("/refresh", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def refresh_user_token(refresh_token=Header(), session: AsyncSession = Depends(get_async_session)):
    return await AuthHandler.get_refresh_token(refresh_token, session)


@auth_protected_router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def fetch_user(user=Depends(SecurityHandler.get_current_user)):
    return user

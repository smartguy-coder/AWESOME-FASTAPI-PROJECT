from fastapi import APIRouter, HTTPException, status, BackgroundTasks, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
import datetime as dt
from app.auth.auth_lib import AuthHandler
from app.auth.security_lib import SecurityHandler
# from app.services import user
# from app.config.security import get_current_user, oauth2_scheme
from app.bl import user as user_bl

# from app.config.database import get_session
from app.schemas.schemas_user import UserResponse, LoginResponse
from app.schemas.schemas_user import RegisterUserRequest, VerifyUserRequest

# from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
from app.database import get_async_session
from app.tasks import background_emails

# from app.schemas.schemas_user import (EmailRequest, RegisterUserRequest, ResetRequest, VerifyUserRequest)


# auth_router = APIRouter(
#     prefix="/users",
#     tags=["Users"],
#     responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
#     dependencies=[Depends(oauth2_scheme), Depends(get_current_user)]
# )

guest_router = APIRouter(
    prefix="/auth",
    tags=["API", "Auth"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@guest_router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def user_login(data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    result = await AuthHandler.get_login_token(data, session)
    return result


# @guest_router.post("/refresh", status_code=status.HTTP_200_OK, response_model=LoginResponse)
# async def refresh_token(refresh_token=Header(), session: Session = Depends(get_session)):
#     return await user.get_refresh_token(refresh_token, session)
#
#
# @guest_router.post("/forgot-password", status_code=status.HTTP_200_OK)
# async def forgot_password(data: EmailRequest, background_tasks: BackgroundTasks,
#                           session: Session = Depends(get_session)):
#     await user.email_forgot_password_link(data, background_tasks, session)
#     return JSONResponse({"message": "A email with password reset link has been sent to you."})
#
#
# @guest_router.put("/reset-password", status_code=status.HTTP_200_OK)
# async def reset_password(data: ResetRequest, session: Session = Depends(get_session)):
#     await user.reset_user_password(data, session)
#     return JSONResponse({"message": "Your password has been updated."})
#
#
# @auth_router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
# async def fetch_user(user=Depends(get_current_user)):
#     return user
#
#
# @auth_router.get("/{pk}", status_code=status.HTTP_200_OK, response_model=UserResponse)
# async def get_user_info(pk, session: Session = Depends(get_session)):
#     return await user.fetch_user_detail(pk, session)

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

router = APIRouter(
    prefix="/api/users",
    tags=["Users", 'API'],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user_account(
        request: Request,
        new_user: RegisterUserRequest,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_async_session)):
    is_login_already_used = await user_bl.get_user_by_email(new_user.email)
    if is_login_already_used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email {new_user.email} already exists"
        )

    is_password_strong = await SecurityHandler.is_password_strong_enough(new_user.password)
    if not is_password_strong:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please, provide a strong password")

    hashed_password = await SecurityHandler.get_password_hash(new_user.password)
    saved_user = await user_bl.create_user(name=new_user.name, email=new_user.email, hashed_password=hashed_password,
                                           session=session)
    background_tasks.add_task(background_emails.send_email_verification, user_email=saved_user.email,
                              user_uuid=saved_user.user_uuid, user_name=saved_user.name, host=request.base_url)
    return saved_user


@router.get("/verify/{user_uuid}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def verify_user_account(user_uuid: str, session: AsyncSession = Depends(get_async_session)):
    user = await user_bl.activate_user_account(user_uuid=user_uuid, session=session)
    return UserResponse(**user.to_dict(), **{'additional_info': {'message': 'Account was activated'}})

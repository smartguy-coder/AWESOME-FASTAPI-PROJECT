from pydantic import BaseModel, EmailStr, Field

from app.settings import settings
from datetime import datetime
from typing import Union
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.schemas.base import BaseResponse


class BaseFields(BaseModel):
    email: EmailStr = Field(description="valid user email", examples=["example@ukr.net"])
    password: str = Field(
        description="strong password", examples=["5fgH=J-*65!"], min_length=settings.PASSWORD_MIX_LENGTH
    )


class RegisterUserRequest(BaseFields):
    name: str = Field(description="Name of a user", examples=["Mark Twen"])


class VerifyUserRequest(BaseModel):
    user_uuid: str


class EmailRequest(BaseModel):
    email: EmailStr


class ResetRequest(BaseFields):
    token: str


class UserResponse(BaseResponse):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    created_at: Union[str, None, datetime] = None
    user_uuid: UUID
    additional_info: dict = {'message': 'Please, check your email box'}


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "Bearer"

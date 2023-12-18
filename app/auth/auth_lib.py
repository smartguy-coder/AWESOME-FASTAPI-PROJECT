from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from app.bl import user as user_bl
from .security_lib import SecurityHandler
from app.settings import settings
from ..models.user import User, UserToken
from app.bl import user_token as user_token_bl
from app.utils import utils_library
from ..schemas.schemas_user import LoginResponse


class AuthHandler:
    secret = settings.JWT_SECRET
    algorithm = settings.JWT_ALGORITHM

    @classmethod
    async def get_login_token(cls, data: OAuth2PasswordRequestForm, session: AsyncSession) -> LoginResponse:
        user = await user_bl.get_user(email=data.username, session=session)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is not registered with us.")

        is_valid_password = await SecurityHandler.verify_password(data.password, user.hashed_password)
        if not is_valid_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password.")

        if not user.verified_at:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account is not verified. Please check your email inbox to verify your account."
            )

        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Your account has been dectivated. Please contact support.")

        token_pair = await cls.generate_token_pair(user, session)
        return token_pair

    @classmethod
    async def generate_token_pair(cls, user: User, session: AsyncSession) -> LoginResponse:
        user_token: UserToken = await user_token_bl.create_user_token(user, session)
        # TODO: do not convert to str?
        access_token_payload = {
            "sub": utils_library.str_encode(str(user.id)),
            'access_key': user_token.access_key,
            'refresh_key': utils_library.str_encode(str(user_token.id)),
            'name': utils_library.str_encode(f"{user.name}"),
        }

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await cls.generate_token(access_token_payload, access_token_expires)

        refresh_token_payload = {
            "sub": utils_library.str_encode(str(user.id)),
            "t": user_token.refresh_key,
            'a': user_token.access_key,
        }
        refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        refresh_token = await cls.generate_token(refresh_token_payload, refresh_token_expires)
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=access_token_expires.seconds,
        )

    @classmethod
    async def generate_token(cls, payload: dict, expiry: timedelta) -> str:
        now = datetime.utcnow()
        time_payload = {
            "exp": now + expiry,
            "iat": now,
        }
        payload.update(time_payload)
        token = jwt.encode(payload, cls.secret, algorithm=cls.algorithm)
        return token

    @classmethod
    async def decode_token(cls, token: str) -> dict:
        try:
            payload = jwt.decode(token, cls.secret, algorithms=[cls.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Signature has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    @classmethod
    async def decode_token_web(cls, token: str | None) -> dict:
        try:
            payload = jwt.decode(token, cls.secret, algorithms=[cls.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return {}
        except jwt.InvalidTokenError:
            return {}

    # @classmethod
    # async def authenticate_user(cls, login: EmailStr, password: str):
    #     user = await user_bl.get_user_by_login(login)
    #     if not (user and await AuthHandler.verify_password(password, user.password)):
    #         raise HTTPException(
    #             status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'Incorrect login "{login}" or password'
    #         )
    #     return user



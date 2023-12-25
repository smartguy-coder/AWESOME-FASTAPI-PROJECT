from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import auth_lib
from app.bl.user_token import get_user_token
from app.database import get_async_session
from app.models.user import User, UserToken
from app.settings import settings
from app.utils import utils_library


class SecurityHandler:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SPECIAL_CHARACTERS = set("@#$%=:?./|~>")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

    @classmethod
    async def get_user_from_token(cls, payload: dict, db: AsyncSession) -> User | None:
        if payload:
            refresh_key = utils_library.str_decode(payload.get("refresh_key") or "")
            user_id = int(utils_library.str_decode(payload.get("sub") or "-1"))
            access_key = payload.get("access_key") or ""
            user_token: UserToken = await get_user_token(
                refresh_key=refresh_key, access_key=access_key, user_id=user_id, session=db
            )
            if user_token:
                return user_token.user
        return None

    @classmethod
    async def get_current_user(
        cls, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_session)
    ):
        payload = await auth_lib.AuthHandler.decode_token(token=token)
        user = await cls.get_user_from_token(payload, db)
        if user:
            return user
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorised.")

    @classmethod
    async def get_password_hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    async def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    async def is_password_strong_enough(cls, password: str) -> bool:
        if len(password) < settings.PASSWORD_MIX_LENGTH:
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char.islower() for char in password):
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not set(password) & cls.SPECIAL_CHARACTERS:
            return False
        return True

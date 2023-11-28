from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app import settings



class AuthHandler:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = settings.settings.TOKEN_SECRET
    algorithm = settings.settings.TOKEN_ALGORITHM

    @classmethod
    async def get_password_hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    async def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    async def encode_token(cls, user_id: int, is_authorised: bool) -> str:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=60),
            'iat': datetime.utcnow(),
            'user_id': user_id,
            'is_authorised': is_authorised

        }
        return jwt.encode(payload, cls.secret, cls.algorithm)

    @classmethod
    async def decode_token_web(cls, token: str | None) -> dict:

        try:
            payload = jwt.decode(token, cls.secret, cls.algorithm)
            return payload
        except jwt.ExpiredSignatureError:
            return {}
        except jwt.InvalidTokenError:
            return {}


class AuthLibrary:

    @classmethod
    async def authenticate_user(cls, login: EmailStr, password: str):
        from dao import get_user_by_login
        user = await get_user_by_login(login)

        if not (user and await AuthHandler.verify_password(password, user.password)):
            return False

        return user

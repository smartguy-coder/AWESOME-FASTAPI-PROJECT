from passlib.context import CryptContext
from app.settings import settings


class SecurityHandler:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SPECIAL_CHARACTERS = set('@#$%=:?./|~>')

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

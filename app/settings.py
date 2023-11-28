import os
from datetime import datetime

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_NAME: str = os.getenv('DATABASE_NAME', '')
    DATABASE_USER: str = os.getenv('DATABASE_USER', '')
    DATABASE_PASSWORD: str = os.getenv('DATABASE_PASSWORD', '')
    DATABASE_HOST: str = os.getenv('DATABASE_HOST', '')
    DATABASE_PORT: int = os.getenv('DATABASE_PORT', '')
    MAX_NOTES_LENGTH: int = 200
    TOKEN_SECRET: str = os.getenv('TOKEN_SECRET') or ''
    TOKEN_ALGORITHM: str = os.getenv('TOKEN_ALGORITHM') or ''

    APP_NAME: str = "Awesome API"
    SENTRY_SDK_DSN: str
    CURRENT_APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    MIN_PASSWORD_LENGTH: int = 8

    @property
    def DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@' \
               f'{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}'


settings = Settings()


class Item(BaseModel):
    names: dict = {
        "name": "default_name",
        "description": "default_description",
        "description1": "default_description1",
        "description2": "default_description2",
        "description3": "default_description3",
    }
    version: str = "0.1.0"
    date: datetime = datetime.now()

    def to_dict(self):
        return {
            "names": self.names,
            "version": self.version,
            "date": self.date.isoformat(),
        }

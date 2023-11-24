import os
from datetime import datetime
from typing import Union
from dotenv import load_dotenv

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings:
    DATABASE_NAME = os.getenv('DATABASE_NAME', '')
    DATABASE_USER = os.getenv('DATABASE_USER', '')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
    DATABASE_HOST = os.getenv('DATABASE_HOST', '')
    DATABASE_PORT = os.getenv('DATABASE_PORT', '')

    TOKEN_SECRET = os.getenv('TOKEN_SECRET') or ''
    TOKEN_ALGORITHM = os.getenv('TOKEN_ALGORITHM') or ''

    APP_NAME = "Awesome API"
    SENTRY_SDK_DSN = ''
    CURRENT_APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    MIN_PASSWORD_LENGTH = 8


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



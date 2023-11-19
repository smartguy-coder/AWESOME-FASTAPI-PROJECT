import os
from dataclasses import dataclass

from dotenv import load_dotenv
import os
from datetime import datetime
from typing import Union

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


@dataclass
class Settings:
    DATABASE_NAME = os.getenv('DATABASE_NAME', '')
    DATABASE_USER = os.getenv('DATABASE_USER', '')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
    DATABASE_HOST = os.getenv('DATABASE_HOST', '')
    DATABASE_PORT = os.getenv('DATABASE_PORT', '')

    TOKEN_SECRET = os.getenv('TOKEN_SECRET') or ''
    TOKEN_ALGORITHM = os.getenv('TOKEN_ALGORITHM') or ''

    MAX_NOTES_LENGTH = 200

    MIN_PASSWORD_LENGTH = 8

    @property
    def DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@' \
               f'{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}'


class Project_info(BaseSettings):
    APP_NAME: str = "Awesome API"
    SENTRY_SDK_DSN: str
    CURRENT_APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # in order to place settings with the main file we dynamically get path to .env
    # model_config = SettingsConfigDict(env_file=os.path.join(os.getcwd(), '.env'))


project_info = Project_info()
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
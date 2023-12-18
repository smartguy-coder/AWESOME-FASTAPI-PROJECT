import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# for working in debug mode
load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "Awesome API"
    SENTRY_SDK_DSN: str
    CURRENT_APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # MongoDB settings
    MONGODB_USER: str
    MONGODB_PASSWORD: str
    MONGODB_URI: str
    MONGODB_SERVER: str
    MONGODB_DB_STORIES: str = "stories"
    MONGODB_COLLECTION_STORIES: str = "user_stories"

    @property
    def MONGODB_URI_FINAL(self) -> str:
        return self.MONGODB_URI.format(
            mongodb_user=self.MONGODB_USER,
            mongodb_password=self.MONGODB_PASSWORD,
            mongodb_server=self.MONGODB_SERVER,
        )

    # Postgres settings
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str

    @property
    def DATABASE_URL(self) -> str:
        # dialect+driver://username:password@host:port/database
        url = (
            f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@"
            f"{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )
        return url

    # in order to place settings with the main file we dynamically get path to .env
    model_config = SettingsConfigDict(env_file=os.path.join(os.getcwd(), ".env"))

    # text field length
    DB_MAX_TEXT_LENGTH: int = 2**6
    PASSWORD_MIX_LENGTH: int = 2**3

    # secrets
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # custom email variables
    EMAIL_TOKEN: str
    EMAIL_USER: str
    IMAP_SERVER: str
    SMTP_SERVER: str



@lru_cache
def get_settings():
    return Settings()


settings = get_settings()

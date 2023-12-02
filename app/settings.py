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
    MONGODB_DB_STORIES: str = 'stories'
    MONGODB_COLLECTION_STORIES: str = 'user_stories'

    @property
    def MONGODB_URI_FINAL(self) -> str:
        return self.MONGODB_URI.format(mongodb_user=self.MONGODB_USER, mongodb_password=self.MONGODB_PASSWORD)

    # in order to place settings with the main file we dynamically get path to .env
    model_config = SettingsConfigDict(env_file=os.path.join(os.getcwd(), ".env"))


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()

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

    # in order to place settings with the main file we dynamically get path to .env
    model_config = SettingsConfigDict(env_file=os.path.join(os.getcwd(), ".env"))


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()

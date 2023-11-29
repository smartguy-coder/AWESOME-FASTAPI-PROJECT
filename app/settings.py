import os
from datetime import datetime
from functools import lru_cache
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

# for working in debug mode
load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "Awesome API"
    SENTRY_SDK_DSN: str
    CURRENT_APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    APP_URL: str = "https://www.google.com/"

    # in order to place settings with the main file we dynamically get path to .env
    model_config = SettingsConfigDict(env_file=os.path.join(os.getcwd(), ".env"))


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()


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

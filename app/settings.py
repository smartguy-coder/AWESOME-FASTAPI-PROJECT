import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime
from pydantic import BaseModel


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
    model_config = SettingsConfigDict(env_file=os.path.join(os.getcwd(), '.env'))


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



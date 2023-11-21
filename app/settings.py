import os
from typing import Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

class Settings(BaseSettings):
    APP_NAME: str = "Awesome API"
    SENTRY_SDK_DSN: str
    CURRENT_APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    USER:str
    PASSWORD:str
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
class Story(BaseModel):
    story_id: str
    text: str = Field("Story", description="Text of the story")
    title: str = Field("Story Title", description="Title of the story")
    tags: List[str] = Field([], description="List of tags")
    utc_time: datetime = Field(default_factory=datetime.utcnow, description="UTC time of the story creation")
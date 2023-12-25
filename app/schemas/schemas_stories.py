from datetime import datetime

from pydantic import BaseModel, Field

from app.constants import Tags
from app.utils import utils_library


class StoryNew(BaseModel):
    text: str = Field(description="Text of the story", examples=["Story text"])
    title: str = Field(description="Title of the story", examples=["Story Title test"])
    tags: list[Tags] = Field([], description="List of tags")


class StoryWithAuthor(StoryNew):
    author: str = Field(description="Author of the story", examples=["Mark Twen"])
    author_id: int = Field(description="User id in DB")


class StorySaved(StoryWithAuthor):
    created_at: datetime = Field(default_factory=datetime.utcnow, description="UTC time of the story creation")
    story_id: str = Field(default_factory=utils_library.create_str_uuid4, description="Story ID")

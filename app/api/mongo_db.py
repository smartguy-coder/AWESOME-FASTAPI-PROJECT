from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4
from pymongo import MongoClient
from app.settings import settings
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from uuid import uuid4

cluster=MongoClient('mongodb+srv://super_user:gTeW01WRUQ9yaP4H@cluster0.sjdq4xj.mongodb.net/retryWrites=true&w=majority')

collection = cluster.test_db.stories
router = APIRouter(
    prefix='',
    tags=['landing'],
)



# Ендпоінт для додавання історій


from fastapi import APIRouter
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4

router = APIRouter()

# Модель для історії
class Story(BaseModel):
    story_id: str = Field(default_factory=lambda: str(uuid4()))
    text: str = Field(..., description="Text of the story")
    title: str = Field(..., description="Title of the story")
    tags: list = Field([], description="List of tags")
    utc_time: datetime = Field(default_factory=datetime.utcnow, description="UTC time of the story creation")

    def to_dict(self):
        return {
            "names": self.names,
            "version": self.version,
            "date": self.date.isoformat(),
        }

@router.post("/add_story")
@router.get("/add_story")
async def add_story_post():
    pattern = {
        "_id": 2,
        "name": "Jeryy",
        "age": 20,
        "balance": 2000,
    }
    collection.insert_one(pattern)
    return True



# Ендпоінт для отримання історій з можливістю фільтрації
@router.get("/get_stories", response_model=List[dict])
def get_stories(skip: int = 0, query: Optional[str] = None):
    if query:
        stories = collection.find({"$or": [
            {"text": {"$regex": query, "$options": "i"}},
            {"title": {"$regex": query, "$options": "i"}}
        ]}).skip(skip).limit(10)
    else:
        stories = collection.find().skip(skip).limit(10)

    return list(stories)
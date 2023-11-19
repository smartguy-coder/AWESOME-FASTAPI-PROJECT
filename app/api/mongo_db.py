from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4
from pymongo import MongoClient
from app.settings import settings
from app.settings import Story
from fastapi.responses import JSONResponse

url=f'mongodb+srv://{settings.USER}:{settings.PASSWORD}@cluster0.sjdq4xj.mongodb.net/retryWrites=true&w=majority'

client = MongoClient(url)
db = client["FASTAPI_JUNIOR_FULL"]
collection = db["stories"]

router = APIRouter(
    prefix='',
    tags=['landing'],
)



# Ендпоінт для додавання історій

@router.post("/add_story", response_model=Story)
def add_story(story: Story):
    story_id = str(uuid4())
    utc_time = datetime.utcnow()
    new_story = {
        "story_id": story_id,
        "text": story.text,
        "title": story.title,
        "tags": story.tags,
        "utc_time": utc_time
    }
    collection.insert_one(new_story)
    return JSONResponse(content={"story_id": story_id, **story.__dict__}, status_code=201)



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
# from fastapi import FastAPI, HTTPException, APIRouter
# from pydantic import BaseModel
# from typing import List, Optional
# from datetime import datetime
# from uuid import UUID, uuid4
# from pymongo import MongoClient
from typing import Any, Optional, List

from pydantic import BaseModel

from app import shemas
from app.settings import settings
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel, Field
# from typing import List
# from datetime import datetime
# from uuid import uuid4
from motor import motor_asyncio


class MongoDBStorage:
    def __init__(self):
        uri = settings.MONGODB_URI_FINAL
        mongo_client = motor_asyncio.AsyncIOMotorClient(uri)
        self.db = mongo_client[settings.MONGODB_DB_STORIES]

    async def get_user_stories_collection(self):
        collection = self.db[settings.MONGODB_COLLECTION_STORIES]
        return collection

    async def add_one_document(self, collection, payload: dict) -> None:
        await collection.insert_one(payload)

    async def find_one_document(self, collection, field: str, value: Any) -> dict:
        search_params = {field: value}
        result = await collection.find_one(search_params)
        return result or {}

    async def get_latest_stories(self, collection) -> List[shemas.StorySaved]:
        latest_stories = collection.find().sort([("_id", -1)]).limit(10)
        stories = []
        async for story in latest_stories:
            story['_id'] = str(story['_id'])
            stories.append(story)
        return stories

mongo_storage = MongoDBStorage()


# # Ендпоінт для отримання історій з можливістю фільтрації
# @router.get("/get_stories", response_model=List[dict])
# def get_stories(skip: int = 0, query: Optional[str] = None):
#     if query:
#         stories = collection.find({"$or": [
#             {"text": {"$regex": query, "$options": "i"}},
#             {"title": {"$regex": query, "$options": "i"}}
#         ]}).skip(skip).limit(10)
#     else:
#         stories = collection.find().skip(skip).limit(10)
#
#     return list(stories)
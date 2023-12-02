from typing import Any, List

from motor import motor_asyncio

from app import schemas
from app.settings import settings


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

    async def get_latest_stories(self, collection) -> List[schemas.StorySaved]:
        latest_stories = collection.find().sort([("_id", -1)]).limit(10)
        stories = []
        async for story in latest_stories:
            story["_id"] = str(story["_id"])
            stories.append(story)
        return stories


mongo_storage = MongoDBStorage()

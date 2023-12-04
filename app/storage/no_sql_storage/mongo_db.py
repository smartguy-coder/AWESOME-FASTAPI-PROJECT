from typing import Any, List

import pymongo
from motor import motor_asyncio

from app import schemas
from app.settings import settings


class MongoDBStorage:
    def __init__(self):
        self.uri = settings.MONGODB_URI_FINAL
        self.mongo_client_async = motor_asyncio.AsyncIOMotorClient(self.uri)
        self.db_async = self.mongo_client_async[settings.MONGODB_DB_STORIES]

        self.mongo_client_sync = pymongo.MongoClient(self.uri)
        self.db_sync = self.mongo_client_sync[settings.MONGODB_DB_STORIES]

    async def get_user_stories_collection_async(self):
        collection = self.db_async[settings.MONGODB_COLLECTION_STORIES]
        return collection

    async def get_user_stories_collection_sync(self):
        collection = self.db_sync[settings.MONGODB_COLLECTION_STORIES]
        return collection

    async def add_one_document(self, collection, payload: dict) -> None:
        await collection.insert_one(payload)

    async def find_one_document(self, collection, field: str, value: Any) -> dict:
        # for some reasons async collection fail in tests
        search_params = {field: value}
        result = collection.find_one(search_params)
        return result or {}

    async def get_latest_stories(self, collection) -> List[schemas.StorySaved]:
        latest_stories = collection.find().sort([("_id", -1)]).limit(10)
        stories = []
        async for story in latest_stories:
            story["_id"] = str(story["_id"])
            stories.append(story)
        return stories


mongo_storage = MongoDBStorage()

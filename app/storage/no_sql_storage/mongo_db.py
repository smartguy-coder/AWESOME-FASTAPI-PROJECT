from typing import Any

import pymongo
from motor import motor_asyncio

from app import schemas
from app.settings import settings


class MongoDBStorage:
    # for some reasons async collection fail in tests, so we use sync func
    # so self.__getattribute__(f"{collection.name}_collection_sync")() allows us to use for tests sync version

    def __init__(self):
        self.uri = settings.MONGODB_URI_FINAL
        self.mongo_client_async = motor_asyncio.AsyncIOMotorClient(self.uri)
        self.db_async = self.mongo_client_async[settings.MONGODB_DB_STORIES]

        self.mongo_client_sync = pymongo.MongoClient(self.uri)
        self.db_sync = self.mongo_client_sync[settings.MONGODB_DB_STORIES]

    async def get_user_stories_collection_async(self):
        collection = self.db_async[settings.MONGODB_COLLECTION_STORIES]
        return collection

    async def user_stories_collection_sync(self):
        collection = self.db_sync[settings.MONGODB_COLLECTION_STORIES]
        return collection

    async def add_one_document(self, collection, payload: dict) -> None:
        await collection.insert_one(payload)

    async def find_one_document(self, collection, field: str, value: Any) -> dict:
        search_params = {field: value}
        try:
            result = await collection.find_one(search_params)
        except RuntimeError:
            collection = await self.__getattribute__(f"{collection.name}_collection_sync")()
            result = collection.find_one(search_params)
        return result or {}

    async def get_latest_stories(self, collection, limit: int, skip: int) -> list[schemas.StorySaved]:
        try:
            latest_stories = await collection.find().sort([("_id", -1)]).limit(limit).skip(skip).to_list(length=limit)
        except RuntimeError:
            collection = await self.__getattribute__(f"{collection.name}_collection_sync")()
            latest_stories = collection.find().sort([("_id", -1)]).limit(limit).skip(skip)
        return latest_stories


mongo_storage = MongoDBStorage()

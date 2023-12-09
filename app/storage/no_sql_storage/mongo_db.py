from typing import Any

import pymongo

from app.settings import settings


class MongoDBStorage:
    def __init__(self):
        self.uri = settings.MONGODB_URI_FINAL
        self.mongo_client_sync = pymongo.MongoClient(self.uri)
        self.db_sync = self.mongo_client_sync[settings.MONGODB_DB_STORIES]

    async def get_user_stories_collection(self):
        collection = self.db_sync[settings.MONGODB_COLLECTION_STORIES]
        return collection

    async def add_one_document(self, collection, payload: dict) -> None:
        collection.insert_one(payload)

    async def find_one_document(self, collection, field: str, value: Any) -> dict:
        search_params = {field: value}
        result = collection.find_one(search_params)
        return result or {}

    async def get_latest_stories(self, collection, limit: int, skip: int) -> list[dict]:
        latest_stories = collection.find().sort([("_id", -1)]).limit(limit).skip(skip)
        return latest_stories


mongo_storage = MongoDBStorage()

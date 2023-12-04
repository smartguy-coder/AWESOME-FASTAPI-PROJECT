from app.schemas import StorySaved
from app.storage.no_sql_storage import mongo_db


async def write_story_into_mongodb(saved_story: StorySaved) -> None:
    collection = await mongo_db.mongo_storage.get_user_stories_collection_async()
    await mongo_db.mongo_storage.add_one_document(collection, saved_story.model_dump())

from app.storage.no_sql_storage import mongo_db
from app.shemas import StorySaved


async def write_story_into_mongodb(saved_story: StorySaved) -> None:
    collection = await mongo_db.mongo_storage.get_user_stories_collection()
    await mongo_db.mongo_storage.add_one_document(collection, saved_story.model_dump())

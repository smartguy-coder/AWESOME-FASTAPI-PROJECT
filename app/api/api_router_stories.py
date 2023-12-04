from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from pydantic_core import ValidationError

from app import schemas
from app.storage.no_sql_storage import mongo_db
from app.tasks import tasks_fastapi

router = APIRouter(
    prefix="/api/stories",
    tags=["stories"],
)


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_story_post(story: schemas.StoryNew, background_tasks: BackgroundTasks) -> schemas.StorySaved:
    saved_story = schemas.StorySaved(**story.model_dump())
    background_tasks.add_task(tasks_fastapi.write_story_into_mongodb, saved_story)
    return saved_story


@router.get("/id/{story_id}")
async def find_story_post(story_id: str) -> schemas.StorySaved:
    collection = await mongo_db.mongo_storage.get_user_stories_collection_sync()
    data = await mongo_db.mongo_storage.find_one_document(collection, "story_id", story_id)

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")
    try:
        return schemas.StorySaved(**data)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Story missing required fields",
        )


@router.get("/latest")
async def get_latest_stories():
    collection = await mongo_db.mongo_storage.get_user_stories_collection_async()
    data = await mongo_db.mongo_storage.get_latest_stories(collection)

    return data

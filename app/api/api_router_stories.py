from fastapi import APIRouter, status, BackgroundTasks, HTTPException
from pydantic_core import ValidationError

from app import shemas
from app.tasks import tasks_fastapi
from app.storage.no_sql_storage import mongo_db

router = APIRouter(
    prefix='/api/stories',
    tags=['stories'],
)


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_story_post(story: shemas.StoryNew, background_tasks: BackgroundTasks) -> shemas.StorySaved:
    saved_story = shemas.StorySaved(**story.model_dump())
    background_tasks.add_task(tasks_fastapi.write_story_into_mongodb, saved_story)
    return saved_story


@router.get("/{story_id}")
async def add_story_post(story_id: str) -> shemas.StorySaved:
    collection = await mongo_db.mongo_storage.get_user_stories_collection()
    data = await mongo_db.mongo_storage.find_one_document(collection, 'story_id', story_id)

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")

    try:
        return shemas.StorySaved(**data)
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Story missing required fields")

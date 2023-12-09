from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, status
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
    collection = await mongo_db.mongo_storage.get_user_stories_collection()
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


@router.get(
    "",
    description="Awesome description [docs](https://fastapi.tiangolo.com) from all over the world with markdown",
    response_description="some useful info for users",
)
async def get_latest_stories(
    limit: int = Query(default=10, ge=1, le=50),
    skip: int = Query(default=0, ge=0),
) -> list[schemas.StorySaved]:
    collection = await mongo_db.mongo_storage.get_user_stories_collection()
    stories = await mongo_db.mongo_storage.get_latest_stories(collection, limit, skip)
    result = []
    for story in stories:
        try:
            result.append(schemas.StorySaved(**story))
        except ValidationError:
            pass
    return result

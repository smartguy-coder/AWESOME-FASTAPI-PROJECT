from fastapi import APIRouter
from fastapi_versioning import version

from app.settings import Item

router = APIRouter(
    prefix='/api',
    tags=['landing'],
)


@router.post('/about')
@router.get('/about')
@version(1)
async def about() -> dict:
    item = Item()
    item_dict = item.to_dict()
    return item_dict

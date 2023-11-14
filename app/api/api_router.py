from fastapi import APIRouter, Request
from fastapi_versioning import version

router = APIRouter(
    prefix='/api',
    tags=['landing'],
)


@router.get('/about')
@version(1)
async def about() -> dict:
    return {}

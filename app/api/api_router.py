from fastapi import APIRouter, Request
from fastapi_versioning import version

router = APIRouter(
    prefix='/api',
    tags=['menu', 'landing'],
)


@router.get('/v1/about')
@version(1)
async def about()->dict:
    1/0
    return {}

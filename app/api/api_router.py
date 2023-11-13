from fastapi import APIRouter, Request
from fastapi_versioning import VersionedFastAPI, version



router = APIRouter(
    prefix='',
    tags=['menu', 'landing'],
)


@router.get('/api/v1/about')
@version(1)
async def about(request: Request):
    return []

from fastapi import APIRouter


router = APIRouter(
    prefix='',
    tags=['menu', 'landing'],
)
@router.get('/api/v1/about')
async def about():
    return []

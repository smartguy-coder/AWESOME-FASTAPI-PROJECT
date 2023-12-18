import datetime as dt

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from sqlalchemy import delete, insert, select, update

from app.database import async_session_maker
from app.models.user import UserToken, User
from sqlalchemy.ext.asyncio import AsyncSession
from app.settings import settings
from app.utils import utils_library


async def create_user_token(user: User, session: AsyncSession):
    refresh_key = utils_library.unique_string(100)
    access_key = utils_library.unique_string(50)
    refresh_token_expires = dt.timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    user_token = UserToken()
    user_token.user_id = user.id
    user_token.refresh_key = refresh_key
    user_token.access_key = access_key
    user_token.expires_at = dt.datetime.utcnow() + refresh_token_expires
    session.add(user_token)
    await session.commit()
    await session.refresh(user_token)
    return user_token

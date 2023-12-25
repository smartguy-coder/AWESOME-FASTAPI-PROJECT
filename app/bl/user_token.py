import datetime as dt

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.user import User, UserToken
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


async def get_user_token(
    *,
    refresh_key: str,
    access_key: str,
    user_id: int,
    session: AsyncSession,
) -> UserToken | None:
    user_token = await session.execute(
        select(UserToken)
        .options(joinedload(UserToken.user))
        .where(
            UserToken.refresh_key == refresh_key,
            UserToken.access_key == access_key,
            UserToken.user_id == user_id,
            UserToken.expires_at > dt.datetime.utcnow(),
        )
    )
    user_token = user_token.scalar_one_or_none()
    return user_token


#
# await db.query(UserToken).options(joinedload(UserToken.user)).filter(
#                 UserToken.access_key == access_key,
#                 UserToken.id == user_token_id,
#                 UserToken.user_id == user_id,
#                 UserToken.expires_at > datetime.utcnow()
#                 ).first()

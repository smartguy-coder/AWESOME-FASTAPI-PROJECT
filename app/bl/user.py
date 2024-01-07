import datetime as dt

from fastapi import HTTPException, status
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app import exceptions
from app.database import async_session_maker
from app.models.user import User


async def create_user(*, name: str, email: str, hashed_password: str, use_two_factor_auth: bool = False, session: AsyncSession):
    """using dependencies https://habr.com/ru/companies/otus/articles/683366/"""
    user = User(
        name=name,
        email=email,
        hashed_password=hashed_password,
        updated_at=dt.datetime.utcnow(),
        use_two_factor_auth=use_two_factor_auth,
    )

    session.add(user)
    try:
        await session.commit()
        await session.refresh(user)
        return user
    except IntegrityError:
        await session.rollback()
        raise exceptions.DuplicatedEntryError("The userdata is already stored")


async def get_user(session: AsyncSession, for_update: bool = False, **search_params) -> User | None:
    if for_update:
        result = await session.execute(select(User).filter_by(**search_params).with_for_update())
    else:
        result = await session.execute(select(User).filter_by(**search_params))
    return result.scalar_one_or_none()


async def activate_user_account(user_uuid: str, session: AsyncSession) -> User:
    user = await get_user(session=session, user_uuid=user_uuid, for_update=True)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provided data is not valid.")
    now = dt.datetime.utcnow()
    user.is_active = True
    user.updated_at = now
    user.verified_at = now
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def fetch_users(skip: int = 0, limit: int = 10):
    async with async_session_maker() as session:
        query = select(User).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()


async def get_user_by_id(user_id: int):
    async with async_session_maker() as session:
        query = select(User).filter_by(id=user_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def get_user_by_email(user_email: str, session: AsyncSession) -> User:
    query = select(User).filter_by(email=user_email)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def update_user(user_id: int, **kwargs):
    async with async_session_maker() as session:
        query = update(User).where(User.id == user_id).values(**kwargs)
        await session.execute(query)
        await session.commit()


async def delete_user(user_id: int):
    async with async_session_maker() as session:
        query = delete(User).where(User.id == user_id)
        await session.execute(query)
        await session.commit()

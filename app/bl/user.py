import datetime as dt

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from sqlalchemy import delete, insert, select, update

from app.database import async_session_maker
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app import exceptions

# async def create_user(*, name: str, email: str, hashed_password: str, background_tasks) -> User:
#     async with async_session_maker() as session:
#         now = dt.datetime.utcnow()
#         query = (
#             insert(User)
#             .values(
#                 name=name,
#                 email=email,
#                 hashed_password=hashed_password,
#                 updated_at=now,
#             )
#             .returning(User.id, User.name, User.is_active, User.created_at, User.user_uuid, User.email)
#         )
#
#         data = await session.execute(query)
#         result = tuple(data)[0]
#         await session.commit()
#         user = User(
#             id=result[0],
#             name=result[1],
#             is_active=result[2],
#             created_at=result[3],
#             user_uuid=result[4],
#             email=result[5],
#             hashed_password=hashed_password,
#             updated_at=now,
#         )
#
#         return user


async def create_user(*, name: str, email: str, hashed_password: str, session: AsyncSession):
    """using dependencies https://habr.com/ru/companies/otus/articles/683366/"""
    # READY
    user = User(
        name=name,
        email=email,
        hashed_password=hashed_password,
        updated_at=dt.datetime.utcnow(),
    )
    session.add(user)
    try:
        await session.commit()
        await session.refresh(user)
        return user
    except IntegrityError as ex:
        await session.rollback()
        raise exceptions.DuplicatedEntryError("The userdata is already stored")


async def get_user(session: AsyncSession, for_update: bool = False, **search_params) -> User | None:
    # READY
    if for_update:
        result = await session.execute(select(User).filter_by(**search_params).with_for_update())
    else:
        result = await session.execute(select(User).filter_by(**search_params))
    return result.scalar_one_or_none()


async def activate_user_account(user_uuid: str, session: AsyncSession) -> User:
    # READY
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
        # print(type(result.scalars().all()[0]))
        # print(result.scalars().all()[0].__dict__)
        return result.scalars().all()


async def get_user_by_id(user_id: int):
    async with async_session_maker() as session:
        query = select(User).filter_by(id=user_id)
        print(query)
        result = await session.execute(query)
        # print(result.first())
        # print(result.scalar_one_or_none())
        return result.scalar_one_or_none()


async def get_user_by_email(user_email: str):
    async with async_session_maker() as session:
        query = select(User).filter_by(email=user_email)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def update_user2(user_id: int, **kwargs):
    async with async_session_maker() as session:
        query = update(User).where(User.id == user_id).values(**kwargs)
        await session.execute(query)
        await session.commit()


async def delete_user(user_id: int):
    async with async_session_maker() as session:
        query = delete(User).where(User.id == user_id)
        print(query)
        await session.execute(query)
        await session.commit()

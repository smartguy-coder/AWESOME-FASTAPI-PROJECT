import datetime

from sqlalchemy import insert, select, update

from database import async_session_maker
from models import User


async def create_user(
        name: str,
        login: str,
        password: str,
):
    async with async_session_maker() as session:
        query = insert(User).values(
            name=name,
            login=login.lower(),
            password=password,

        ).returning(User.id, User.login, User.name)
        data = await session.execute(query)
        await session.commit()
        return data


async def fetch_users(skip: int = 0, limit: int = 10) -> list:
    async with async_session_maker() as session:
        query = select(User).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()


async def get_user_by_id(user_id: int) -> list:
    async with async_session_maker() as session:
        query = select(User).filter_by(id=user_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def get_user_login_by_id(user_id: int) -> list:
    async with async_session_maker() as session:
        query = select(User).filter_by(id=user_id)
        result = await session.execute(query)
        return result.scalar_one_or_none().login


async def get_user_by_login(user_login: str) -> list:
    async with async_session_maker() as session:
        query = select(User).filter_by(login=user_login.lower())
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def get_user_id_by_login(user_login: str) -> int:
    async with async_session_maker() as session:
        query = select(User).filter_by(login=user_login.lower())
        result = await session.execute(query)
        result = result.scalar_one_or_none()
        if result:
            return result.id
        return False


async def get_user_uuid_by_id(user_idd: int):
    async with async_session_maker() as session:
        query = select(User).filter_by(id=user_idd)
        result = await session.execute(query)
        return result.scalar_one_or_none().user_uuid


async def update_user_last_login(user_id: int):
    async with async_session_maker() as session:
        query = update(User).where(User.id == user_id).values(last_login=datetime.datetime.utcnow())

        await session.execute(query)
        await session.commit()


async def main():
    # await asyncio.gather(
    #     create_user(
    #         name='name1',
    #         login='login2',
    #         password='password1'
    #     )
    # )
    # await asyncio.gather(fetch_users())

    # await asyncio.gather(update_user(222))
    # await asyncio.gather(delete_user(2))
    # hashed_password = await AuthHandler.get_password_hash("password2")
    # totp = str(await create_otp("login2"))
    # user_data = await create_user(
    #     name='nnnaaammmeee2',
    #     login="login2",
    #     password=hashed_password,
    #     totp=totp,
    # )
    # print(await asyncio.gather(get_user_by_id(2)))

    await update_user_last_login(11)
    # print(await get_user_id_by_login('yaroslavshym@gamail.com'))

# asyncio.run(main())

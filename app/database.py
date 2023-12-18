from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker, create_async_engine)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from app.settings import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)
# expire_on_commit=False. Это связано с тем, что в настройках async мы не хотим, чтобы SQLAlchemy выдавал новые SQL-запросы к базе данных при обращении к уже закоммиченным объектам.



async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency"""
    async with async_session_maker() as session:
        yield session


# def get_session() -> Generator:
#     ????????
#     session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)
#     try:
#         yield session
#     finally:
#         session.close()


class Base(DeclarativeBase):
    pass

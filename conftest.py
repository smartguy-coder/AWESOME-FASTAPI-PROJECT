# # import asyncio
# import datetime as dt
# from typing import AsyncGenerator
#
# import pytest
# from faker import Faker
# from fastapi import Depends
# from httpx import AsyncClient
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from app.database import get_async_session
# from app.main import app
# from app.schemas.schemas_stories import StoryNew
# from app.schemas.schemas_user import RegisterUserRequest
#
# fake_data = Faker(locale="uk_UA")
#
#
# @pytest.fixture(params=["asyncio"], scope="session")
# def anyio_backend(request):
#     return request.param
#
#
# @pytest.fixture(scope="class")
# def new_story() -> StoryNew:
#     test_story = StoryNew(
#         author=fake_data.name(),
#         title="Test title CI-CD",
#         text=f"Test text CI-CD at {dt.datetime.utcnow()}",
#     )
#     return test_story
#
#
# @pytest.fixture(scope="session")
# def new_user_payload() -> RegisterUserRequest:
#     new_user = RegisterUserRequest(
#         name=fake_data.name(),
#         email=fake_data.email(),
#         password="5fgH=J-*65!546HJjhh5545*-",  # strong password
#     )
#     return new_user
#
#
# @pytest.fixture(scope="session")
# async def user(session: AsyncSession = Depends(get_async_session)):
#     yield 9
#
#
# @pytest.fixture(scope="session")
# async def ac_protected() -> AsyncGenerator[AsyncClient, None]:
#     async with AsyncClient(app=app, base_url="http://") as ac:
#         print("попытка авторизации")
#         response = await ac.post(
#             "auth/login",
#             data={
#                 "username": "user@example.com",
#                 "password": "string",
#             },
#         )
#         if response.status_code in [200, 204]:
#             yield ac
#         else:
#             raise Exception(f"fail to create auth session {response.status_code}")

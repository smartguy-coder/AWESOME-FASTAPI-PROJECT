# import asyncio
import datetime as dt

import pytest
from faker import Faker

# from app.main import app
from app.schemas.schemas_stories import StoryNew
from app.schemas.schemas_user import RegisterUserRequest
from app.utils import utils_library

# from typing import AsyncIterator


# from httpx import AsyncClient


fake_data = Faker(locale="uk_UA")


@pytest.fixture(params=["asyncio"], scope="session")
def anyio_backend(request):
    return request.param


# @pytest.fixture(scope="class")
# async def client() -> AsyncIterator[AsyncClient]:
#     async with AsyncClient(app=app, base_url="http://") as client:
#         yield client


@pytest.fixture(scope="class")
def new_story() -> StoryNew:
    test_story = StoryNew(
        author=fake_data.name(),
        title="Test title CI-CD",
        text=f"Test text CI-CD at {dt.datetime.utcnow()}",
    )
    return test_story


@pytest.fixture(scope="session")
def new_user_request() -> RegisterUserRequest:
    new_user = RegisterUserRequest(
        name=fake_data.name(),
        email=fake_data.email(),
        password=utils_library.make_randon_assii_string(10),
    )
    return new_user


# @pytest.fixture
# def event_loop():
#     loop = asyncio.get_event_loop()
#     yield loop
#     # cleanly_shutdown(loop)
#
#
# def pytest_sessionfinish(session, exitstatus):
#     asyncio.get_event_loop().close()


# @pytest.fixture(scope="class")
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     # loop.close()

#
# from datetime import datetime
# import sys
# import os
# from typing import Generator
#
# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from starlette.testclient import TestClient
#
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#
# from app.main import app
# from app.config.email import fm
# from app.config.database import Base, get_session
# from app.models.user import User
# from app.config.security import hash_password
# from app.services.user import _generate_tokens
#
# USER_NAME = "Keshari Nandan"
# USER_EMAIL = "keshari@describly.com"
# USER_PASSWORD = "123#Describly"
#
# engine = create_engine("sqlite:///./fastapi.db")
# SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
# @pytest.fixture(scope="function")
# def test_session() -> Generator:
#     session = SessionTesting()
#     try:
#         yield session
#     finally:
#         session.close()
#
#
# @pytest.fixture(scope="function")
# def app_test():
#     Base.metadata.create_all(bind=engine)
#     yield app
#     Base.metadata.drop_all(bind=engine)
#
#
# @pytest.fixture(scope="function")
# def client(app_test, test_session):
#     def _test_db():
#         try:
#             yield test_session
#         finally:
#             pass
#
#     app_test.dependency_overrides[get_session] = _test_db
#     fm.config.SUPPRESS_SEND = 1
#     return TestClient(app_test)
#
# @pytest.fixture(scope="function")
# def auth_client(app_test, test_session, user):
#     def _test_db():
#         try:
#             yield test_session
#         finally:
#             pass
#
#     app_test.dependency_overrides[get_session] = _test_db
#     fm.config.SUPPRESS_SEND = 1
#     data = _generate_tokens(user, test_session)
#     client = TestClient(app_test)
#     client.headers['Authorization'] = f"Bearer {data['access_token']}"
#     return client
#
#
# @pytest.fixture(scope="function")
# def inactive_user(test_session):
#     model = User()
#     model.name = USER_NAME
#     model.email = USER_EMAIL
#     model.password = hash_password(USER_PASSWORD)
#     model.updated_at = datetime.utcnow()
#     model.is_active = False
#     test_session.add(model)
#     test_session.commit()
#     test_session.refresh(model)
#     return model
#
# @pytest.fixture(scope="function")
# def user(test_session):
#     model = User()
#     model.name = USER_NAME
#     model.email = USER_EMAIL
#     model.password = hash_password(USER_PASSWORD)
#     model.updated_at = datetime.utcnow()
#     model.verified_at = datetime.utcnow()
#     model.is_active = True
#     test_session.add(model)
#     test_session.commit()
#     test_session.refresh(model)
#     return model
#
# @pytest.fixture(scope="function")
# def unverified_user(test_session):
#     model = User()
#     model.name = USER_NAME
#     model.email = USER_EMAIL
#     model.password = hash_password(USER_PASSWORD)
#     model.updated_at = datetime.utcnow()
#     model.is_active = True
#     test_session.add(model)
#     test_session.commit()
#     test_session.refresh(model)
#     return model

# import asyncio
import datetime as dt

import pytest

# from fastapi.testclient import TestClient
#
# from app.main import app
from app.schemas import StoryNew

# @pytest.fixture(scope="session")
# def client():
#     client_ = TestClient(app)
#     yield client_
#     del client_


@pytest.fixture(scope="class")
def new_story() -> StoryNew:
    test_story = StoryNew(
        author="Test author CI-CD",
        title="Test title CI-CD",
        text=f"Test text CI-CD at {dt.datetime.utcnow()}",
    )
    return test_story


# @pytest.fixture(scope="class")
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     # loop.close()

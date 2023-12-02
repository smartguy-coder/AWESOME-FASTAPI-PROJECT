import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas import StoryNew


@pytest.fixture(scope="session")
def client():
    yield TestClient(app)


@pytest.fixture(scope="class")
def new_story() -> StoryNew:
    test_story = StoryNew(
        author="Test author",
        title="Test title",
        text="Test text",
    )
    return test_story

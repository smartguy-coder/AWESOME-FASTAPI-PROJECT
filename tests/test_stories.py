import pytest
from fastapi import status
from httpx import AsyncClient

from app.main import app


class TestAddStory:
    @pytest.fixture(scope="class", autouse=True)
    @classmethod
    def setup_class(cls, new_story):
        cls.URL_ADD_STORY: str = "/api/stories/add"
        cls.URL_FIND_ONE_STORY: str = "/api/stories/id/{story_id}"
        cls.UUID_NEW_STORY: dict = {"story_id": None}
        cls.story = new_story
        cls.base_url = "http://"

    async def test_add_story_no_body(self):
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(self.URL_ADD_STORY)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert not response.json()["detail"][0]["input"]

    async def test_add_story_success(self):
        data = self.story.model_dump()
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(self.URL_ADD_STORY, json=data)
        assert response.status_code == status.HTTP_201_CREATED
        self.UUID_NEW_STORY["story_id"] = response.json()["story_id"]

    async def test_find_created_story_success(self):
        url = self.URL_FIND_ONE_STORY.format(story_id=self.UUID_NEW_STORY["story_id"])
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["author"] == self.story.author
        assert data["text"] == self.story.text
        assert data["title"] == self.story.title

    async def test_find_story_no_id(self):
        url = self.URL_FIND_ONE_STORY.split("{")[0]
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestGetStories:
    @pytest.fixture(scope="class", autouse=True)
    @classmethod
    def setup_class(cls, new_story):
        cls.URL_GET_STORIES: str = "/api/stories/"
        cls.base_url = "http://"

    async def test_success_get_stories(self):
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(self.URL_GET_STORIES)
        assert response.status_code == status.HTTP_200_OK
        data: list[dict] = response.json()
        assert isinstance(data, list)
        assert isinstance(data[0], dict)
        assert "text" in data[0].keys()

    @pytest.mark.parametrize("bad_param", [{"limit": -5}, {"limit": 500}, {"skip": -5}, {"skip": "five"}])
    async def test_bad_query_params(self, bad_param: dict):
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(self.URL_GET_STORIES, params=bad_param)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

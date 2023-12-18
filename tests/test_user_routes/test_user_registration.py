import pytest
from fastapi import status
from httpx import AsyncClient

from app.main import app


class TestUserRegistration:
    @pytest.fixture(scope="class", autouse=True)
    @classmethod
    def setup_class(cls, new_user_request):
        cls.URL_USER_REGISTER: str = "/users/create"
        cls.UUID_NEW_STORY: dict = {"story_id": None}
        cls.user_data = new_user_request
        cls.base_url = "http://"

    async def test_create_user_no_body(self):
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(self.URL_USER_REGISTER)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert not response.json()["detail"][0]["input"]

    async def test_create_user_success(self):
        data = self.user_data.model_dump()
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(self.URL_USER_REGISTER, json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert "password" not in response.json()

    # async def test_create_user_with_existing_email(self):
    #     data = self.user_data.model_dump()
    #     async with AsyncClient(app=app, base_url=self.base_url) as ac:
    #         response = await ac.post(self.URL_USER_REGISTER, json=data)
    #     print(response.json(), 888888888888)
    #     assert response.status_code == status.HTTP_201_CREATED


class TestUserRegistration2:
    @pytest.fixture(scope="class", autouse=True)
    @classmethod
    def setup_class(cls, new_user_request):
        cls.URL_USER_REGISTER: str = "/users/create"
        cls.user_data = new_user_request
        cls.base_url = "http://"

    # def test_create_user_with_existing_email(self):
    #     from fastapi.testclient import TestClient
    #
    #     client = TestClient(app)
    #     data = self.user_data.model_dump()
    #
    #     response = client.post(self.URL_USER_REGISTER, json=data)
    #     print(response.json(), 888888888888)
    #     assert response.status_code == status.HTTP_201_CREATED

    #
    #
    # def test_create_user_with_invalid_email(client):
    #     data = {
    #         "name": "Keshari Nandan",
    #         "email": "keshari.com",
    #         "password": USER_PASSWORD
    #     }
    #     response = client.post("/users/", json=data)
    #     assert response.status_code != 201
    #
    #
    # def test_create_user_with_empty_password(client):
    #     data = {
    #         "name": "Keshari Nandan",
    #         "email": USER_EMAIL,
    #         "password": ""
    #     }
    #     response = client.post("/users/", json=data)
    #     assert response.status_code != 201
    #
    #
    # def test_create_user_with_numeric_password(client):
    #     data = {
    #         "name": "Keshari Nandan",
    #         "email": USER_EMAIL,
    #         "password": "1232382318763"
    #     }
    #     response = client.post("/users/", json=data)
    #     assert response.status_code != 201
    #
    #
    # def test_create_user_with_char_password(client):
    #     data = {
    #         "name": "Keshari Nandan",
    #         "email": USER_EMAIL,
    #         "password": "asjhgahAdF"
    #     }
    #     response = client.post("/users/", json=data)
    #     assert response.status_code != 201
    #
    #
    # def test_create_user_with_alphanumeric_password(client):
    #     data = {
    #         "name": "Keshari Nandan",
    #         "email": USER_EMAIL,
    #         "password": "sjdgajhGG27862"
    #     }
    #     response = client.post("/users/", json=data)
    #     assert response.status_code != 201

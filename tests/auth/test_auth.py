# import pytest
# from fastapi import status
# from httpx import AsyncClient
#
# from app.main import app
#
#
# class TestUserAuth:
#     @pytest.fixture(scope="class", autouse=True)
#     @classmethod
#     def setup_class(cls, new_user_payload):
#         cls.URL_CREATE_USER: str = "/api/users/create"
#         cls.new_user_payload = new_user_payload.model_dump()
#         cls.base_url = "http://"
#
#     async def test_create_new_user(self):
#         async with AsyncClient(app=app, base_url=self.base_url) as ac:
#             response = await ac.post(self.URL_CREATE_USER, json=self.new_user_payload)
#         assert response.status_code == status.HTTP_201_CREATED

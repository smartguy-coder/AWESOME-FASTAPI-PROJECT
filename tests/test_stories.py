from fastapi import status


async def test_add_story_no_body(client):
    result = client.post("/api/stories/add")
    assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert not result.json()["detail"][0]["input"]


async def test_add_story_success(client, new_story):
    data = new_story.model_dump()
    result = client.post("/api/stories/add", json=data)
    print(result.json())
    assert result.status_code == status.HTTP_201_CREATED

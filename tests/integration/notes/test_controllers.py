import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
async def test_can_create_note(async_test_client: AsyncClient) -> None:
    # given
    payload = {
        "owner_id": 1,
        "header": "header",
        "content": "content",
        "tags": [],
    }

    # when
    response = await async_test_client.post("/notes", json=payload)

    # then
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
async def test_can_get_note(async_test_client: AsyncClient) -> None:
    # when
    response = await async_test_client.get(f"/notes/1")

    # then
    assert response.status_code == status.HTTP_200_OK


# def test_should_return_404_if_user_does_not_exist(test_client: TestClient, seed_db: list[dict[str, str]]) -> None:
#     # when
#     response = test_client.get(f"/users/{ObjectId()}")

#     # then
#     assert response.status_code == status.HTTP_404_NOT_FOUND


# def test_can_get_all_useres(test_client: TestClient, seed_db: list[dict[str, str]]) -> None:
#     # when
#     response = test_client.get("/users")

#     # then
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.json()) == len(seed_db)


# def test_can_update_user(test_client: TestClient, seed_db: list[dict[str, str]]) -> None:
#     # when
#     user_id = seed_db[0]["id"]
#     payload = {"name": "Morning start-up", "day": "Monday", "time": "9:00-10:00", "coach": "Nina G.", "description": ""}
#     response = test_client.put(f"/users/{user_id}", json=payload)

#     # then
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["name"] == payload["name"]

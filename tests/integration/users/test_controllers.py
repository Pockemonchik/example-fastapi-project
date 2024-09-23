from bson.objectid import ObjectId
from fastapi import status
from fastapi.testclient import TestClient


def test_can_create_user(test_client: TestClient) -> None:
    # given
    payload = {
        "name": "Pilates",
        "day": "Monday",
        "time": "10:30-11:30",
        "coach": "Simon W.",
        "description": "Try pilates in our gym",
    }

    # when
    response = test_client.post("/users", json=payload)

    # then
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()


def test_can_get_user(test_client: TestClient, seed_db: list[dict[str, str]]) -> None:
    # when
    user_id = seed_db[0]["id"]
    response = test_client.get(f"/users/{user_id}")

    # then
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == seed_db[0]


def test_should_return_404_if_user_does_not_exist(test_client: TestClient, seed_db: list[dict[str, str]]) -> None:
    # when
    response = test_client.get(f"/users/{ObjectId()}")

    # then
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_can_get_all_useres(test_client: TestClient, seed_db: list[dict[str, str]]) -> None:
    # when
    response = test_client.get("/users")

    # then
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(seed_db)


def test_can_update_user(test_client: TestClient, seed_db: list[dict[str, str]]) -> None:
    # when
    user_id = seed_db[0]["id"]
    payload = {"name": "Morning start-up", "day": "Monday", "time": "9:00-10:00", "coach": "Nina G.", "description": ""}
    response = test_client.put(f"/users/{user_id}", json=payload)

    # then
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == payload["name"]

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_notes_db")
async def test_can_create_note(async_test_client: AsyncClient) -> None:
    # given
    payload = {
        "owner_id": 1,
        "header": "header",
        "content": "content",
        "tags": [],
    }

    # when
    response = await async_test_client.post("/notes/", json=payload)

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


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_notes_db")
async def test_can_update_note(async_test_client: AsyncClient) -> None:
    # given
    payload = {
        "owner_id": 1,
        "header": "header_updated",
        "content": "content_updated",
    }

    # when
    response = await async_test_client.put(url=f"/notes/1", json=payload)
    print(response)
    # then
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_notes_db")
async def test_can_delete_note(async_test_client: AsyncClient) -> None:
    # given

    # when
    response = await async_test_client.delete(url=f"/notes/1")
    print(response)
    # then
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_notes_db")
async def test_should_return_404_if_note_does_not_exist(async_test_client: AsyncClient) -> None:
    # when
    response = await async_test_client.get(f"/notes/1234")

    # then
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_notes_db")
async def test_can_get_all_notes(async_test_client: AsyncClient) -> None:
    # given

    # when
    response = await async_test_client.get(f"/notes/")

    # then
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_notes_db")
async def test_can_get_notes_by_any_field(async_test_client: AsyncClient) -> None:
    # given

    # when
    response = await async_test_client.get(f"/notes/filter/?header=header")

    # then
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) >= 1


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_notes_db")
async def test_can_get_notes_by_tag_name(async_test_client: AsyncClient) -> None:
    # given

    # when
    response = await async_test_client.get(f"/notes/by_tag_name/?tag_name=header")

    # then
    assert response.status_code == status.HTTP_200_OK

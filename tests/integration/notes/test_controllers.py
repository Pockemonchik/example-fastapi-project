import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.parametrize(
    "client_inject",
    [
        "async_test_client",
        "async_test_client_mongo",
    ],
    ids=[
        "Postgres inject",
        "Mongo inject",
    ],
)
async def test_can_create_note(client_inject: AsyncClient, request: pytest.FixtureRequest) -> None:
    # given
    payload = {
        "owner_id": 1,
        "header": "header",
        "content": "content",
        "tags": [],
    }
    client = request.getfixturevalue(client_inject)
    # when
    response = await client.post("/notes/", json=payload)

    # then
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.parametrize(
    "client_inject",
    [
        "async_test_client",
        "async_test_client_mongo",
    ],
    ids=[
        "Postgres inject",
        "Mongo inject",
    ],
)
async def test_can_get_all_notes(client_inject: AsyncClient, request: pytest.FixtureRequest) -> None:
    # given

    # when
    client = request.getfixturevalue(client_inject)
    response = await client.get(f"/notes/")

    # then
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.parametrize(
    "client_inject",
    [
        "async_test_client",
        "async_test_client_mongo",
    ],
    ids=[
        "Postgres inject",
        "Mongo inject",
    ],
)
async def test_can_get_note(client_inject: AsyncClient, request: pytest.FixtureRequest) -> None:
    # when
    client = request.getfixturevalue(client_inject)
    response = await client.get(f"/notes/")
    id = response.json()[0]["id"]
    response = await client.get(f"/notes/{id}")
    print("get_note resp", response.json())
    # then
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.parametrize(
    "client_inject",
    [
        "async_test_client",
        "async_test_client_mongo",
    ],
    ids=[
        "Postgres inject",
        "Mongo inject",
    ],
)
async def test_can_update_note(client_inject: AsyncClient, request: pytest.FixtureRequest) -> None:
    # given
    payload = {
        "owner_id": 1,
        "header": "header_updated",
        "content": "content_updated",
    }

    # when
    client = request.getfixturevalue(client_inject)
    response = await client.get(f"/notes/")
    id = response.json()[0]["id"]
    response = await client.put(url=f"/notes/{id}", json=payload)
    # then
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.parametrize(
    "client_inject",
    [
        "async_test_client",
        "async_test_client_mongo",
    ],
    ids=[
        "Postgres inject",
        "Mongo inject",
    ],
)
async def test_can_delete_note(client_inject: AsyncClient, request: pytest.FixtureRequest) -> None:
    # given

    # when
    client = request.getfixturevalue(client_inject)
    response = await client.get(f"/notes/")
    id = response.json()[0]["id"]
    response = await client.delete(url=f"/notes/{id}")
    # then
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.parametrize(
    "client_inject",
    [
        "async_test_client",
        "async_test_client_mongo",
    ],
    ids=[
        "Postgres inject",
        "Mongo inject",
    ],
)
async def test_should_return_404_if_note_does_not_exist(
    client_inject: AsyncClient, request: pytest.FixtureRequest
) -> None:
    # when
    client = request.getfixturevalue(client_inject)
    print("client", client)
    response = await client.get(f"/notes/86fa687a4e244963eac54ab4")

    # then
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.parametrize(
    "client_inject",
    [
        "async_test_client",
        "async_test_client_mongo",
    ],
    ids=[
        "Postgres inject",
        "Mongo inject",
    ],
)
async def test_can_get_notes_by_any_field(client_inject: AsyncClient, request: pytest.FixtureRequest) -> None:
    # given

    # when
    client = request.getfixturevalue(client_inject)
    response = await client.get(f"/notes/filter/?header=test1header")
    print("any_field resp", response.json())
    # then
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) >= 1


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.parametrize(
    "client_inject",
    [
        "async_test_client",
        "async_test_client_mongo",
    ],
    ids=[
        "Postgres inject",
        "Mongo inject",
    ],
)
async def test_can_get_notes_by_tag_name(client_inject: AsyncClient, request: pytest.FixtureRequest) -> None:
    # given
    tag_name = "test2tag1"
    # when
    client = request.getfixturevalue(client_inject)
    response = await client.get(f"/notes/by_tag_name/?tag_name={tag_name}")

    # then
    assert response.status_code == status.HTTP_200_OK

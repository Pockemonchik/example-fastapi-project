import pytest
from pymongo.database import Database

from src.notes.application.dto import CreateNoteDTO, UpdateNoteDTO
from src.notes.domain.note import Note
from src.notes.infrastructure.mongo_note_repo import NoteMongoRepository


@pytest.mark.usefixtures("seed_notes_mongo_db")
@pytest.mark.asyncio(scope="module")
async def test_can_get_all_notes(async_mongo_db: Database) -> None:
    # given
    repo = NoteMongoRepository(async_mongo_db)

    # when
    result = await repo.get_all()

    # then
    assert len(result) >= 3


@pytest.mark.usefixtures("seed_notes_mongo_db")
@pytest.mark.asyncio(scope="module")
async def test_can_add_one_note(async_mongo_db: Database) -> None:
    # given
    repo = NoteMongoRepository(async_mongo_db)
    # создается без тэгов, логика их добавления в services
    data = {
        "owner_id": 1,
        "header": "header inserted",
        "content": "content inserded",
        "tags": [],
    }

    new_note = CreateNoteDTO(**data)
    # when
    result = await repo.add_one(new_note=new_note)
    print("add_one result", result)
    # then
    assert type(result) == Note
    assert result.header == "header inserted"


@pytest.mark.usefixtures("seed_notes_mongo_db")
@pytest.mark.asyncio(scope="module")
async def test_can_delete_one_note(async_mongo_db: Database) -> None:
    # given
    repo = NoteMongoRepository(async_mongo_db)
    result = await async_mongo_db["notes"].find({"header": "header inserted"}).to_list()
    id = result[0]["_id"]
    # when
    result = await repo.delete_one(id=id)
    print("test_can_delete_one_note result", result)
    # then
    assert type(result) == int
    assert result == 1


@pytest.mark.usefixtures("seed_notes_mongo_db")
@pytest.mark.asyncio(scope="module")
async def test_can_update_one_note(async_mongo_db: Database) -> None:
    # given
    repo = NoteMongoRepository(async_mongo_db)
    # создается без тэгов, логика их добавления в services
    data = {
        "owner_id": 1,
        "header": "header updated",
        "content": "content updated",
    }

    new_note = UpdateNoteDTO(**data)
    # when
    result = await repo.add_one(new_note=new_note)
    print("add_one result", result)
    # then
    assert type(result) == Note
    assert result.header == "header updated"
    assert result.content == "content updated"


@pytest.mark.usefixtures("seed_notes_mongo_db")
@pytest.mark.asyncio(scope="module")
async def test_can_filter_notes_by_any_field(async_mongo_db: Database) -> None:
    # given
    repo = NoteMongoRepository(async_mongo_db)
    # создается без тэгов, логика их добавления в services
    params = {
        "header": "header updated",
    }
    # when
    result = await repo.filter_by_field(params=params)
    # then
    assert type(result) == list
    assert len(result) >= 3
    assert type(result[0]) == Note
    assert result[0].owner_id == 1


@pytest.mark.usefixtures("seed_notes_mongo_db")
@pytest.mark.asyncio(scope="module")
async def test_can_filter_notes_by_tags(async_mongo_db: Database) -> None:
    # given
    repo = NoteMongoRepository(async_mongo_db)
    tag_name = "test1tag1"
    # when
    result = await repo.filter_by_tag_name(tag_name=tag_name)
    # then
    assert type(result) == list
    assert type(result[0]) == Note

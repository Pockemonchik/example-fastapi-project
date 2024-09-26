import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from src.notes.application.dto import CreateNoteDTO, UpdateNoteDTO
from src.notes.domain.note import Note
from src.notes.infrastructure.postgres_note_repo import NotePostgresRepository


@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.asyncio
async def test_can_get_all_notes(postgres_async_session: async_scoped_session[AsyncSession]) -> None:
    # given
    repo = NotePostgresRepository(postgres_async_session)

    # when
    result = await repo.get_all()

    # then
    assert len(result) >= 3


@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.asyncio
async def test_can_get_one_note(postgres_async_session: async_scoped_session[AsyncSession]) -> None:
    # given
    repo = NotePostgresRepository(postgres_async_session)

    # when
    result = await repo.get_one(id=1)

    # then
    assert type(result) == Note
    assert result.id == 1


@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.asyncio
async def test_can_add_one_note(postgres_async_session: async_scoped_session[AsyncSession]) -> None:
    # given
    repo = NotePostgresRepository(postgres_async_session)
    # создается без тэгов, логика их добавления в services
    data = {
        "owner_id": 1,
        "header": "header",
        "content": "content",
        "tags": [],
    }

    new_note = CreateNoteDTO(**data)
    # when
    result = await repo.add_one(new_note=new_note)
    print("add_one result", result)
    # then
    assert type(result) == Note
    assert result.header == "header"


@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.asyncio
async def test_can_update_one_note(postgres_async_session: async_scoped_session[AsyncSession]) -> None:
    # given
    repo = NotePostgresRepository(postgres_async_session)

    data = {
        "owner_id": 1,
        "header": "header_updated",
        "content": "content_updated",
    }

    note_update = UpdateNoteDTO(**data)
    # when
    result = await repo.update_one(id=1, note_update=note_update)

    # then
    assert type(result) == Note
    assert result.header == "header_updated"
    assert result.content == "content_updated"


@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.asyncio
async def test_can_delete_one_note(postgres_async_session: async_scoped_session[AsyncSession]) -> None:
    # given
    repo = NotePostgresRepository(postgres_async_session)

    # when
    result = await repo.delete_one(id=1)

    # then
    assert type(result) == int
    assert result == 1


@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.asyncio
async def test_can_filter_by_header(postgres_async_session: async_scoped_session[AsyncSession]) -> None:
    # given
    repo = NotePostgresRepository(postgres_async_session)

    # when
    result = await repo.filter_by_header(header="header")

    # then
    assert type(result) == list
    assert len(result) >= 1


@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.asyncio
async def test_can_filter_by_tag_name(postgres_async_session: async_scoped_session[AsyncSession]) -> None:
    # given
    repo = NotePostgresRepository(postgres_async_session)

    # when
    result = await repo.filter_by_tag_name(tag_name="test2tag1")

    # then
    assert type(result) == list
    assert len(result) == 1

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from src.notes.application.dto import CreateNoteDTO, NoteDTO, UpdateNoteDTO
from src.notes.application.note_service import NoteService
from src.notes.infrastructure.postgres_note_repo import NotePostgresRepository


@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.asyncio(scope="module")
async def test_can_get_all_notes(postgres_async_session: async_scoped_session[AsyncSession]) -> None:
    # given
    repo = NotePostgresRepository(postgres_async_session)
    service = NoteService(note_repo=repo)

    # when
    result = await service.get_all()

    # then
    assert len(result) >= 3


@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.asyncio(scope="module")
async def test_can_get_note_by_id(postgres_async_session: async_scoped_session[AsyncSession]) -> None:
    # given
    repo = NotePostgresRepository(postgres_async_session)
    service = NoteService(note_repo=repo)
    # when

    result = await service.get_note_by_id(id=1)

    # then
    assert type(result) == NoteDTO
    assert result.id == 1


@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.asyncio(scope="module")
async def test_can_create_note(postgres_async_session: async_scoped_session[AsyncSession]) -> None:
    # given
    repo = NotePostgresRepository(postgres_async_session)
    service = NoteService(note_repo=repo)
    # создается без тэгов, логика их добавления в services
    data = {
        "owner_id": 1,
        "header": "header",
        "content": "content",
        "tags": [],
    }

    new_note = CreateNoteDTO(**data)
    # when
    result = await service.create_note(input_dto=new_note)
    print("add_one result", result)
    # then
    assert type(result) == NoteDTO
    assert result.header == "header"


@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.asyncio(scope="module")
async def test_can_update_one_note(postgres_async_session: async_scoped_session[AsyncSession]) -> None:
    # given
    repo = NotePostgresRepository(postgres_async_session)
    service = NoteService(note_repo=repo)
    data = {
        "owner_id": 1,
        "header": "header_updated",
        "content": "content_updated",
    }

    note_update = UpdateNoteDTO(**data)

    # when
    result = await service.update_note(id=1, input_dto=note_update)

    # then
    assert type(result) == NoteDTO
    assert result.header == "header_updated"
    assert result.content == "content_updated"


@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.asyncio(scope="module")
async def test_can_delete_note(postgres_async_session: async_scoped_session[AsyncSession]) -> None:
    # given
    repo = NotePostgresRepository(postgres_async_session)
    service = NoteService(note_repo=repo)

    # when
    result = await service.delete_note(id=1)

    # then
    assert type(result) == int
    assert result == 1


@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.asyncio(scope="module")
async def test_can_get_notes_by_field(postgres_async_session: async_scoped_session[AsyncSession]) -> None:
    # given
    repo = NotePostgresRepository(postgres_async_session)
    service = NoteService(note_repo=repo)

    # when
    result = await service.get_notes_by_filter(
        params={
            "header": "header",
            "content": "content",
        }
    )

    # then
    assert type(result) == list
    assert len(result) >= 1


@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.asyncio(scope="module")
async def test_can_get_notes_by_tag_name(postgres_async_session: async_scoped_session[AsyncSession]) -> None:
    # given
    repo = NotePostgresRepository(postgres_async_session)
    service = NoteService(note_repo=repo)

    # when
    result = await service.get_notes_by_tag_name(tag_name="test2tag1")

    # then
    assert type(result) == list
    assert len(result) == 1

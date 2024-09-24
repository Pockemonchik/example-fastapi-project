import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from src.notes.infrastructure.postgres_note_repo import NotePostgresRepository


@pytest.mark.usefixtures("seed_notes_db")
@pytest.mark.asyncio
async def test_can_get_all_notes(postgres_async_session: async_scoped_session[AsyncSession]) -> None:
    # given
    repo = NotePostgresRepository(postgres_async_session)

    # when
    result = await repo.get_all()

    # then
    assert len(result) == 3

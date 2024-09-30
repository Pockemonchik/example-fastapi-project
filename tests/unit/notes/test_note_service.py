from datetime import datetime
from unittest import mock

import pytest

from src.notes.application.note_service import NoteService
from src.notes.domain.note import Note
from src.notes.domain.note_repo import INoteRepository


@pytest.mark.asyncio(scope="module")
async def test_can_get_all_notes() -> None:
    # given
    repo_mock = mock.AsyncMock(spec=INoteRepository)
    repo_mock.get_all.return_value = [
        Note(
            id=1,
            owner_id=1,
            header="header",
            content="content",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
    ]
    service = NoteService(note_repo=repo_mock)

    # when
    result = await service.get_all()

    # then
    assert len(result) == 1

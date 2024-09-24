import datetime

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.notes.infrastructure.note_model import NoteModel


@pytest.fixture()
@pytest.mark.asyncio
async def seed_notes_db(postgres_async_session: AsyncSession) -> None:
    note_data = [
        {
            "id": 1,
            "owner_id": 1,
            "header": "header",
            "content": "content",
            "create_date": datetime.datetime.now(),
            "last_change_date": datetime.datetime.now(),
        },
        {
            "id": 2,
            "owner_id": 1,
            "header": "header",
            "content": "content",
            "create_date": datetime.datetime.now(),
            "last_change_date": datetime.datetime.now(),
        },
        {
            "id": 3,
            "owner_id": 1,
            "header": "header",
            "content": "content",
            "create_date": datetime.datetime.now(),
            "last_change_date": datetime.datetime.now(),
        },
    ]
    async with postgres_async_session() as session:
        exist_data = await session.execute(select(NoteModel))
        if not exist_data:
            for note in note_data:
                print("type(session)", type(session), session)
                session.add(NoteModel(**note))
                print(f"add note id -> {note['id']}")
            await session.commit()

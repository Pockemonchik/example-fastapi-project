import datetime

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.notes.infrastructure.models.note_model import NoteModel
from src.notes.infrastructure.models.tag_model import TagModel


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
            "tags": ["super", "secret"],
        },
        {
            "id": 2,
            "owner_id": 1,
            "header": "header",
            "content": "content",
            "create_date": datetime.datetime.now(),
            "last_change_date": datetime.datetime.now(),
            "tags": ["super2", "secret2"],
        },
        {
            "id": 3,
            "owner_id": 1,
            "header": "header",
            "content": "content",
            "create_date": datetime.datetime.now(),
            "last_change_date": datetime.datetime.now(),
            "tags": [],
        },
    ]
    async with postgres_async_session() as session:
        exist_data = await session.execute(select(NoteModel))
        if not exist_data.all():
            for note in note_data:
                model_tags = []
                for tag in note["tags"]:
                    model_tags.append(TagModel(name=tag))
                note["tags"] = model_tags
                session.add(NoteModel(**note))
            await session.commit()

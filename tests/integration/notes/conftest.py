import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.notes.infrastructure.models.note_model import NoteModel
from src.notes.infrastructure.models.tag_model import TagModel


@pytest.fixture(scope="module")
@pytest.mark.asyncio(scope="module")
async def seed_notes_db(postgres_async_session: AsyncSession) -> None:
    note_data = [
        {
            "id": 1,
            "owner_id": 1,
            "header": "test1header",
            "content": "test1content",
            "tags": ["test1tag1", "test1tag2"],
        },
        {
            "id": 2,
            "owner_id": 1,
            "header": "test2header",
            "content": "test2content",
            "tags": ["test2tag1", "test2tag2"],
        },
        {
            "id": 222,
            "owner_id": 1,
            "header": "test3header",
            "content": "test3content",
            "tags": [],
        },
    ]
    async with postgres_async_session() as session:
        id_tuple = tuple(note["id"] for note in note_data)
        exist_data = await session.execute(select(NoteModel).filter(NoteModel.id.in_(id_tuple)))
        result_id_list = []
        result_id_list = [note.id for note in exist_data.scalars().all()]
        print("result_id_list ", result_id_list)
        for note in note_data:
            if note["id"] not in result_id_list:
                print("add new", note["id"])
                model_tags = []
                for tag in note["tags"]:
                    model_tags.append(TagModel(name=tag))
                note["tags"] = model_tags
                session.add(NoteModel(**note))
        await session.commit()

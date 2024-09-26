from typing import Any, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.notes.application.dto import CreateNoteDTO, UpdateNoteDTO
from src.notes.domain.note import Note
from src.notes.domain.note_repo import INoteRepository
from src.notes.infrastructure.models.note_model import NoteModel


class NotePostgresRepository(INoteRepository):
    model = NoteModel

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_one(self, id: int) -> Note | Any:
        """Получение заметки по id"""
        obj = await self.session.get(
            self.model,
            id,
            options=[joinedload(self.model.tags)],
        )  # type: ignore
        await self.session.commit()
        if obj == None:
            await self.session.close()
            return None
        else:
            await self.session.close()
            return obj.to_domain()

    async def get_all(self) -> List[Note] | None:
        """Получение всех заметок"""
        stmt = select(self.model).options(joinedload(self.model.tags))  # type: ignore
        obj = await self.session.execute(stmt)
        await self.session.close()
        if obj:
            note_list = [row[0].to_domain() for row in obj.unique().all()]
            return note_list
        else:
            return None

    async def add_one(self, new_note: CreateNoteDTO) -> Note | Any:
        """Добавление заметки, без тэгов"""
        new_note_model = self.model(**new_note.model_dump())
        self.session.add(new_note_model)  # type: ignore
        await self.session.commit()
        await self.session.close()
        return new_note_model.to_domain()

    async def update_one(self, id: int, note_update: UpdateNoteDTO) -> Note | Any:
        """Обновление заметки, без тэгов"""
        obj = await self.session.get(
            self.model,
            id,
            options=[joinedload(self.model.tags)],
        )  # type: ignore
        if obj == None:
            await self.session.close()
            return None
        else:
            for name, value in note_update.model_dump().items():
                setattr(obj, name, value)
            result = obj.to_domain()
            await self.session.commit()
            await self.session.close()
            return result

    async def delete_one(self, id: int) -> int | None:

        obj = await self.session.get(
            self.model,
            id,
            options=[joinedload(self.model.tags)],
        )  # type: ignore
        await self.session.commit()
        if obj == None:
            await self.session.close()
            return None
        else:
            # obj.tags = []
            await self.session.delete(obj)
            await self.session.commit()
            await self.session.close()
            return id

from typing import Any, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from src.notes.domain.note import Note
from src.notes.domain.note_repo import INoteRepository
from src.notes.infrastructure.note_model import NoteModel


class NotePostgresRepository(INoteRepository):
    model = NoteModel

    def __init__(self, session: async_scoped_session[AsyncSession]):
        self.session = session

    async def get_one(self, id: int) -> Note | Any:
        obj = await self.session.get(self.model, id)  # type: ignore
        await self.session.commit()
        if obj == None:
            await self.session.close()
            return None
        else:
            print(type(obj))
            print(type(self.session))
            await self.session.close()
            return obj.to_domain()

    async def get_all(self) -> List[Note] | None:
        stmt = select(self.model)  # type: ignore
        obj = await self.session.execute(stmt)
        await self.session.close()
        print(type(obj))
        print(type(self.session))
        if obj:
            note_list = [row[0].to_domain() for row in obj.all()]
            return note_list
        else:
            return None

    async def add_one(self, new_note: Note) -> Note | Any:

        new_note_model = NoteModel(**vars(new_note))
        await self.session.add(new_note_model)  # type: ignore
        await self.session.commit()
        await self.session.close()
        return new_note_model.to_domain()

    # async def update_one(self, id: int, data: Note) -> Any:

    #     obj = await self.session.get(self.model, id)
    #     if obj == None:
    #         await self.session.close()
    #         return None
    #     else:
    #         for name, value in vars(data).items():
    #             setattr(obj, name, value)
    #         await self.session.commit()
    #         return obj.to_domain()

    # async def delete_one(self, id: int) -> int | None:

    #     obj = await self.session.get(self.model, id)
    #     if obj == None:
    #         await self.session.close()
    #         return None
    #     else:
    #         await self.session.delete(obj)
    #         await self.session.commit()
    #         await self.session.close()
    #         return id

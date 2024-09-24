from abc import ABC, abstractmethod

from src.notes.domain.note import Note


class INoteRepository(ABC):
    @abstractmethod
    async def get_one(self, note_id: int) -> Note | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[Note]:
        pass

    @abstractmethod
    async def add_one(self, note: Note) -> Note:
        pass

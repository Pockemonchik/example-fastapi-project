from abc import ABC, abstractmethod
from typing import Any, List

from src.notes.application.dto import UpdateNoteDTO
from src.notes.domain.note import Note


class INoteRepository(ABC):
    @abstractmethod
    async def get_one(self, id: int) -> Note | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[Note]:
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, new_note: Note) -> Note:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id: int, note_update: UpdateNoteDTO) -> Note | Any:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int) -> int | None:
        raise NotImplementedError

    @abstractmethod
    async def filter_by_field(self, header: str) -> List[Note] | None:
        raise NotImplementedError

    @abstractmethod
    async def filter_by_tag_name(self, tag_name: str) -> List[Note] | None:
        raise NotImplementedError

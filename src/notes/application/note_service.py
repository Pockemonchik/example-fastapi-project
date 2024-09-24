from typing import List

from kink import inject

from src.core.clock import Clock
from src.notes.application.dto import CreateNoteDTO, NoteDTO
from src.notes.domain.note import Note
from src.notes.domain.note_repo import INoteRepository


@inject
class NoteService:
    def __init__(
        self,
        note_repo: INoteRepository,
        clock: Clock = Clock.system_clock(),
    ) -> None:
        self._note_repo = note_repo
        self._clock = clock

    async def create(self, input_dto: CreateNoteDTO) -> NoteDTO:
        note = Note(**input_dto.model_dump())

        result = await self._note_repo.add_one(note)

        return NoteDTO(**vars(result))

    async def get_one_by_id(self, id: int) -> NoteDTO:
        note_model_obj = await self._note_repo.get_one(note_id=id)
        note_dto = NoteDTO(**vars(note_model_obj))
        return note_dto

    async def get_all(self) -> List[NoteDTO]:
        notes = await self._note_repo.get_all()
        note_dto_list = [NoteDTO(**vars(note_model_obj)) for note_model_obj in notes]
        return note_dto_list

from typing import List

from dependency_injector.wiring import inject

from src.notes.application.dto import CreateNoteDTO, NoteDTO, TagDTO
from src.notes.domain.note import Note
from src.notes.domain.note_repo import INoteRepository


@inject
class NoteService:
    def __init__(
        self,
        note_repo: INoteRepository,
    ) -> None:
        self.note_repo = note_repo

    @staticmethod
    def note_entity_to_dto(note_entity_obj: Note) -> NoteDTO:
        tag_names = []
        if note_entity_obj.tags:
            tag_names = [TagDTO(**vars(tag)) for tag in note_entity_obj.tags]
        note_dict = vars(note_entity_obj)
        note_dict["tags"] = tag_names
        note_dto = NoteDTO(**note_dict)
        return note_dto

    async def create_note(self, input_dto: CreateNoteDTO) -> NoteDTO:
        new_note = await self.note_repo.add_one(new_note=input_dto)
        return self.note_entity_to_dto(new_note)

    async def update_note(self, id: int, input_dto: CreateNoteDTO) -> NoteDTO:
        new_note = await self.note_repo.update_one(id=id, note_update=input_dto)
        return self.note_entity_to_dto(new_note)

    async def get_note_by_id(self, id: int) -> NoteDTO:
        note_entity_obj = await self.note_repo.get_one(id=id)
        note_dto = self.note_entity_to_dto(note_entity_obj)
        return note_dto

    async def get_all(self) -> List[NoteDTO]:
        notes = await self.note_repo.get_all()
        note_dto_list = [self.note_entity_to_dto(note_entity_obj) for note_entity_obj in notes]
        return note_dto_list

    async def delete_note(self, id: int) -> int | None:
        result = await self.note_repo.delete_one(id=id)
        return result

    async def get_notes_by_filter(self, params: dict) -> List[Note] | None:
        notes = await self.note_repo.filter_by_field(params)
        note_dto_list = [self.note_entity_to_dto(note_entity_obj) for note_entity_obj in notes]
        return note_dto_list

    async def get_notes_by_tag_name(self, tag_name: str) -> List[Note] | None:
        notes = await self.note_repo.filter_by_tag_name(tag_name)
        note_dto_list = [self.note_entity_to_dto(note_entity_obj) for note_entity_obj in notes]
        return note_dto_list

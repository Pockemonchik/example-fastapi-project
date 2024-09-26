import datetime
from typing import List

from pydantic import BaseModel


class CreateNoteDTO(BaseModel):
    owner_id: int
    header: str
    content: str
    tags: List[str] | None = None


class NoteDTO(BaseModel):
    note_id: int
    owner_id: int
    header: str
    content: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    tags: List[str]


class UpdateNoteDTO(BaseModel):
    owner_id: int
    header: str
    content: str


class CreateTagDTO(BaseModel):
    name: str

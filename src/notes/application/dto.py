import datetime
from typing import List

from pydantic import BaseModel


class CreateTagDTO(BaseModel):
    name: str


class TagDTO(BaseModel):
    id: int
    name: str


class NoteDTO(BaseModel):
    id: int
    owner_id: int
    header: str
    content: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    tags: List[TagDTO]


class UpdateNoteDTO(BaseModel):
    owner_id: int
    header: str
    content: str


class CreateNoteDTO(BaseModel):
    owner_id: int
    header: str
    content: str
    tags: List[str] | None = None

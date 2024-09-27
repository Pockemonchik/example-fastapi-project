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


class FilterNoteDTO(BaseModel):
    id: int | None = None
    owner_id: int | None = None
    header: str | None = None
    content: str | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None


class CreateNoteDTO(BaseModel):
    owner_id: int
    header: str
    content: str
    tags: List[str] | None = None

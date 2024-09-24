import datetime
from typing import List, Optional

from pydantic import BaseModel


class CreateNoteDTO(BaseModel):
    note_id: int
    owner_id: int
    header: str
    content: str
    create_date: datetime.datetime
    last_change_date: datetime.datetime
    tags: List[str]


class NoteDTO(BaseModel):
    note_id: int
    owner_id: int
    header: str
    content: str
    create_date: datetime.datetime
    last_change_date: datetime.datetime
    tags: List[str]


class ChangeContentDTO(BaseModel):
    note_id: Optional[str] = None
    content: str

import datetime
from typing import List

from src.notes.domain.tag import Tag


class Note:
    def __init__(
        self,
        note_id: int,
        owner_id: int,
        header: str,
        content: str,
        created_at: datetime.datetime,
        updated_at: datetime.datetime,
        tags: List[Tag] | None = None,
    ) -> None:
        self.id = note_id
        self.owner_id = owner_id
        self.created_at = created_at
        self.header = header
        self.content = content
        self.updated_at = updated_at
        self.tags = tags

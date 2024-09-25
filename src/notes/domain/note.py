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
        create_date: datetime.datetime,
        last_change_date: datetime.datetime,
        tags: List[Tag] | None = None,
    ) -> None:
        self.id = note_id
        self.owner_id = owner_id
        self.create_date = create_date
        self.header = header
        self.content = content
        self.last_change_date = last_change_date
        self.tags = tags

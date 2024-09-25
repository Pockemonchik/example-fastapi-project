import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Mapped, relationship

from src.core.base_model import BaseModel
from src.notes.domain.note import Note

if TYPE_CHECKING:
    from src.notes.infrastructure.models.note_tag_association_model import NoteTagAssociationModel
    from src.notes.infrastructure.models.tag_model import TagModel


class NoteModel(BaseModel):
    __tablename__ = "notes"
    owner_id: Mapped[int]
    header: Mapped[str]
    content: Mapped[str]
    create_date: Mapped[datetime.datetime]
    last_change_date: Mapped[datetime.datetime]
    tags: Mapped[Optional[list["TagModel"]]] = relationship(
        secondary="note_tag_association",
        back_populates="notes",
    )

    def to_domain(self) -> Note:
        return Note(
            note_id=self.id,
            owner_id=self.owner_id,
            create_date=self.create_date,
            header=self.header,
            content=self.content,
            last_change_date=self.last_change_date,
            tags=[tag.to_domain() for tag in self.tags],
        )

    def __str__(self) -> str:
        return str(self.id)

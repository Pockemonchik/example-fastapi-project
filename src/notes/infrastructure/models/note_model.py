from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    tags: Mapped[Optional[list["TagModel"]]] = relationship(
        secondary="note_tag_association",
        back_populates="notes",
    )

    def to_domain(self) -> Note:
        return Note(
            id=self.id,
            owner_id=self.owner_id,
            created_at=self.created_at,
            header=self.header,
            content=self.content,
            updated_at=self.updated_at,
            tags=[tag.to_domain() for tag in self.tags],
        )

    def __str__(self) -> str:
        return str(self.id)

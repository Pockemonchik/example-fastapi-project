from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from src.core.base_model import BaseModel
from src.notes.domain.note import Note
from src.notes.domain.tag import Tag

if TYPE_CHECKING:
    from src.notes.infrastructure.models.note_model import NoteModel
    from src.notes.infrastructure.models.note_tag_association_model import NoteTagAssociationModel


class TagModel(BaseModel):
    __tablename__ = "tags"
    name: Mapped[str]

    notes: Mapped[list["NoteModel"]] = relationship(
        secondary="note_tag_association",
        back_populates="tags",
    )

    def to_domain(self) -> Note:
        return Tag(
            tag_id=self.id,
            name=self.name,
        )

    def __str__(self) -> str:
        return str(self.id)

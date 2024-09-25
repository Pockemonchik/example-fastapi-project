from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base_model import BaseModel


class NoteTagAssociationModel(BaseModel):
    __tablename__ = "note_tag_association"
    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))

import datetime

from sqlalchemy.orm import Mapped, mapped_column

from src.core.base_model import Base
from src.notes.domain.note import Note


class NoteModel(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int]
    header: Mapped[str]
    content: Mapped[str]
    create_date: Mapped[datetime.datetime]
    last_change_date: Mapped[datetime.datetime]

    def to_domain(self) -> Note:
        return Note(
            note_id=self.id,
            owner_id=self.owner_id,
            create_date=self.create_date,
            header=self.header,
            content=self.content,
            last_change_date=self.last_change_date,
            tags=[],
        )

    def __str__(self) -> str:
        return str(self.id)

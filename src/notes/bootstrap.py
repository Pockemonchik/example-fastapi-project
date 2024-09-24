import os

from kink import di

from src.core.db_postgres import AsyncPostgresDatabaseManager
from src.notes.application.note_service import NoteService
from src.notes.domain.note_repo import INoteRepository
from src.notes.infrastructure.postgres_note_repo import NotePostgresRepository


def bootstrap_di() -> None:
    db = AsyncPostgresDatabaseManager(
        url=os.environ.get("DB_URL", "locahost"),
        echo=bool(os.environ.get("DB_ECHO", False)),
    )
    repository = NotePostgresRepository(session=db.get_scoped_session())

    di[INoteRepository] = repository
    di[NoteService] = NoteService(note_repo=repository)

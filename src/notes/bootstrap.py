import os

from dependency_injector import containers, providers

from src.core.db_postgres import AsyncPostgresDatabaseManager
from src.notes.application.note_service import NoteService
from src.notes.infrastructure.postgres_note_repo import NotePostgresRepository


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["src.notes.controllers"])  # or "users" in your case

    # Define configuration
    config = providers.Configuration()

    db = AsyncPostgresDatabaseManager(
        url=os.environ.get("DB_URL", "postgresql+asyncpg://example_app:example_app@127.0.0.1:5436/example_app"),
        echo=bool(os.environ.get("DB_ECHO", False)),
    )
    async_session = providers.Factory(
        db.get_scoped_session,
    )

    repository = providers.Factory(
        NotePostgresRepository,
        session=async_session,
    )
    service = providers.Factory(NoteService, note_repo=repository)

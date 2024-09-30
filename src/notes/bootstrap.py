import os

from dependency_injector import containers, providers
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from src.core.db_postgres import AsyncPostgresDatabaseManager
from src.notes.application.note_service import NoteService
from src.notes.infrastructure.mongo_note_repo import NoteMongoRepository
from src.notes.infrastructure.postgres_note_repo import NotePostgresRepository


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["src.notes.controllers"])  # or "users" in your case

    # Define configuration
    config = providers.Configuration()

    # Postgres inject
    db = AsyncPostgresDatabaseManager(
        url=os.environ.get("DB_URL", "postgresql+asyncpg://example_app:example_app@127.0.0.1:5436/example_app"),
        echo=bool(os.environ.get("DB_ECHO", False)),
    )
    async_session = providers.Factory(
        db.get_scoped_session,
    )

    posgtgres_repository = providers.Factory(
        NotePostgresRepository,
        session=async_session,
    )

    # Mongo inject

    async_mongo_client = providers.Factory(
        AsyncMongoClient,
        "mongodb://localhost:27017/",
    )

    async_mongo_db = providers.Factory(
        AsyncDatabase,
        client=async_mongo_client,
        name="exaple_app_test",
    )

    mongo_repository = providers.Factory(
        NoteMongoRepository,
        db=async_mongo_db,
    )
    repository = mongo_repository
    # Service inject
    # service = providers.Factory(NoteService, note_repo=posgtgres_repository)
    service = providers.Factory(NoteService, note_repo=repository)

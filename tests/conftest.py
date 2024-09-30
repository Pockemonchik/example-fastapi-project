from typing import Iterator

import nest_asyncio
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from pymongo import AsyncMongoClient, MongoClient
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.database import Database
from pytest import MonkeyPatch
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db_postgres import AsyncPostgresDatabaseManager
from src.main import app
from src.notes.application.note_service import NoteService
from src.notes.infrastructure.mongo_note_repo import NoteMongoRepository
from src.notes.infrastructure.postgres_note_repo import NotePostgresRepository

nest_asyncio.apply()


@pytest.fixture()
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="module")
async def async_test_client():
    db = AsyncPostgresDatabaseManager(
        url="postgresql+asyncpg://example_app:example_app@127.0.0.1:5436/example_app",
        echo=True,
    )
    async_session = db.get_scoped_session()

    posgtgres_repository = NotePostgresRepository(session=async_session)

    service = NoteService(note_repo=posgtgres_repository)
    app.container.service.override(service)
    with app.container.repository.override(posgtgres_repository):
        async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
            yield client


@pytest.fixture(scope="module")
async def async_test_client_mongo():
    async_mongo_client = AsyncMongoClient("mongodb://localhost:27017/")

    async_mongo_db = AsyncDatabase(
        client=async_mongo_client,
        name="exaple_app_test",
    )

    mongo_repository = NoteMongoRepository(
        db=async_mongo_db,
    )

    service = NoteService(note_repo=mongo_repository)
    app.container.service.override(service)
    with app.container.repository.override(mongo_repository):
        async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
            yield client


@pytest.fixture()
def mongodb(monkeypatch: MonkeyPatch) -> Iterator[Database]:
    monkeypatch.setenv("MONGO_DATABASE_NAME", "exaple_app_test")

    mongo_client: MongoClient = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5)

    database = mongo_client.get_database("exaple_app_test")

    yield database

    mongo_client.drop_database("exaple_app_test")


@pytest.fixture(scope="module")
def async_mongo_db() -> Iterator[Database]:

    async_mongo_client: AsyncMongoClient = AsyncMongoClient("mongodb://localhost:27017/")

    database = async_mongo_client["exaple_app_test"]

    yield database

    # mongo_client.drop_database("exaple_app_test")


@pytest.fixture(scope="module")
def test_db_manager() -> AsyncPostgresDatabaseManager:
    db = AsyncPostgresDatabaseManager(
        url="postgresql+asyncpg://example_app:example_app@127.0.0.1:5436/example_app",
        echo=True,
    )
    return db


@pytest.fixture(scope="module")
def postgres_async_session(test_db_manager) -> AsyncSession:
    return test_db_manager.get_scoped_session()

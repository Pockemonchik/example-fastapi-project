from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from pymongo import MongoClient
from pymongo.database import Database
from pytest import MonkeyPatch
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db_postgres import AsyncPostgresDatabaseManager
from src.main import app


@pytest.fixture()
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="module")
async def async_test_client():
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
def test_db_manager() -> AsyncPostgresDatabaseManager:
    db = AsyncPostgresDatabaseManager(
        url="postgresql+asyncpg://example_app:example_app@127.0.0.1:5436/example_app",
        echo=True,
    )
    return db


@pytest.fixture(scope="module")
def postgres_async_session(test_db_manager) -> AsyncSession:
    return test_db_manager.get_scoped_session()

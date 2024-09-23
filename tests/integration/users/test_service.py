import pytest
from bson import ObjectId
from pymongo.database import Database

from src.users.errors import UserMongoSchemaNotFound
from src.users.models import UserMongoCreateOrUpdateSchema, UserMongoSchema
from src.users.service import UserMongoService


@pytest.mark.usefixtures("seed_db")
def test_can_get_all_sorted_by_day(mongodb: Database) -> None:
    # given
    service = UserMongoService(mongodb)

    # when
    result = service.get_all()

    # then
    assert len(result) == 5
    assert result[0].name == "Cross fit kids"
    assert result[4].name == "MMA"


@pytest.mark.usefixtures("seed_db")
def test_can_get_one(mongodb: Database) -> None:
    # given
    service = UserMongoService(mongodb)

    # when
    user = service.get(ObjectId("63500520c1f28686b7d7da2c"))

    # then
    assert isinstance(user, UserMongoSchema)
    assert user.name == "Pilates 1"
    assert user.day == "Monday"
    assert user.description == "test 1"


@pytest.mark.usefixtures("seed_db")
def test_should_raise_an_error_if_user_does_not_exist(mongodb: Database) -> None:
    # given
    service = UserMongoService(mongodb)

    # expect
    with pytest.raises(UserMongoSchemaNotFound):
        service.get(ObjectId())


def test_can_create_new_user(mongodb: Database) -> None:
    # given
    service = UserMongoService(mongodb)
    collection = mongodb.get_collection("users")

    # when
    result = service.create(
        UserMongoCreateOrUpdateSchema(
            name="Test123",
            day="Monday",
            time="10:30",
            coach="John Doe",
        )
    )

    # then

    documents = list(collection.find({}))
    assert isinstance(result, UserMongoSchema)
    assert len(documents) == 1
    assert documents[0]["name"] == "Test123"


@pytest.mark.usefixtures("seed_db")
def test_can_update_user(mongodb: Database) -> None:
    # given
    service = UserMongoService(mongodb)
    collection = mongodb.get_collection("users")

    # when
    result = service.update(
        "63500520c1f28686b7d7da2c",
        UserMongoCreateOrUpdateSchema(
            name="Test",
            day="Monday",
            time="10:30",
            coach="John Doe",
            description="123",
        ),
    )

    # then
    document = collection.find_one({"_id": ObjectId("63500520c1f28686b7d7da2c")})
    assert isinstance(result, UserMongoSchema)
    assert result.name == "Test"
    assert document["name"] == "Test"  # type: ignore


@pytest.mark.usefixtures("seed_db")
def test_can_delete(mongodb: Database) -> None:
    # given
    service = UserMongoService(mongodb)
    collection = mongodb.get_collection("users")

    # when
    service.delete("63500520c1f28686b7d7da2c")

    # then
    documents = list(collection.find({}))
    assert len(documents) == 4
    assert "63500520c1f28686b7d7da2c" not in [str(document["_id"]) for document in documents]

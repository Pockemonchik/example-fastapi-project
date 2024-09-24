from bson.objectid import ObjectId
from pymongo.database import Database

from src.users.errors import UserMongoSchemaNotFound
from src.users.models import UserMongoCreateOrUpdateSchema, UserMongoSchema


class UserMongoService:
    def __init__(self, database: Database) -> None:
        self._collection = database.get_collection("users")

    def get(self, user_id: ObjectId) -> UserMongoSchema:
        document = self._collection.find_one({"_id": user_id})

        if not document:
            raise UserMongoSchemaNotFound(f"User with id={user_id} was not found!")

        document["id"] = str(document["_id"])
        return UserMongoSchema(**document)

    def get_all(self) -> list[UserMongoSchema]:
        useres = []
        documents = self._collection.find({})
        for document in documents:
            document["id"] = str(document["_id"])
            useres.append(UserMongoSchema(**document))

        days_order = {
            "Monday": 1,
            "Tuesday": 2,
            "Wednesday": 3,
            "Thursday": 4,
            "Friday": 5,
            "Saturday": 6,
            "Sunday": 7,
        }

        return sorted(useres, key=lambda x: (days_order.get(x.day), x.time))

    def create(self, user_request: UserMongoCreateOrUpdateSchema) -> UserMongoSchema:
        document = user_request.model_dump()
        result = self._collection.insert_one(document)

        return self.get(result.inserted_id)

    def update(self, user_id: str, user_request: UserMongoCreateOrUpdateSchema) -> UserMongoSchema:
        user = self.get(ObjectId(user_id))
        user.name = user_request.name
        user.day = user_request.day
        user.time = user_request.time
        user.coach = user_request.coach
        user.description = user_request.description

        new_values = user.model_dump()
        del new_values["id"]

        self._collection.update_one({"_id": ObjectId(user_id)}, {"$set": new_values})
        return user

    def delete(self, user_id: str) -> None:
        self._collection.delete_one({"_id": ObjectId(user_id)})

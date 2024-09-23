from src.core.db import get_mongo_database
from src.users.service import UserMongoService


class Deps:
    @staticmethod
    def get_user_service() -> UserMongoService:
        return UserMongoService(get_mongo_database())

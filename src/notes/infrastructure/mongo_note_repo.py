from datetime import datetime
from typing import Any, List

from bson import ObjectId
from pymongo.database import Database

from src.notes.application.dto import CreateNoteDTO, UpdateNoteDTO
from src.notes.domain.errors import NoteError, NoteErrorNotFound
from src.notes.domain.note import Note
from src.notes.domain.note_repo import INoteRepository
from src.notes.domain.tag import Tag


class NoteMongoRepository(INoteRepository):

    def __init__(self, db: Database):
        self._collection = db.get_collection("notes")

    @staticmethod
    def document_to_domain(document: dict):
        note = Note(**document)
        if "tags" in document.keys():
            tags = [Tag(tag_id=None, name=tag_name) for tag_name in note.tags]
            note.tags = tags
        return note

    async def get_one(self, id: str) -> Note | Any:
        """Получение заметки по id"""
        print("get_1 mongo id", id)
        document = await self._collection.find_one({"_id": ObjectId(id)})

        if not document:
            raise NoteErrorNotFound(f"Note with id={id} was not found!")

        document["id"] = str(document["_id"])
        del document["_id"]
        return self.document_to_domain(document)

    async def get_all(self) -> List[Note] | None:
        """Получение всех заметок"""
        documents = await self._collection.find({}).to_list()

        for document in documents:
            document["id"] = str(document["_id"])
            del document["_id"]

        return [self.document_to_domain(document) for document in documents]

    async def add_one(self, new_note: CreateNoteDTO) -> Note | Any:
        """Добавление заметки, без тэгов"""
        document = new_note.model_dump()
        document["created_at"] = datetime.now()
        document["updated_at"] = datetime.now()
        result = await self._collection.insert_one(document)

        return await self.get_one(id=result.inserted_id)

    async def update_one(self, id: str, note_update: UpdateNoteDTO) -> Note | Any:
        """Обновление заметки, без тэгов"""
        new_values = {"$set": note_update.model_dump()}
        result = await self._collection.update_one({"_id": ObjectId(id)}, new_values)
        if result.modified_count == 1:
            return await self.get_one(id=id)
        else:
            raise NoteError(f"err when del")

    async def delete_one(self, id: str) -> int | None:
        """Удаление заметки, без тэгов"""
        result = await self._collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count

    async def filter_by_field(self, params: dict) -> List[Note] | None:
        """Фильтр любому поллю кроме тэгов"""
        params = {key: value for (key, value) in params.items() if value != None}
        documents = await self._collection.find(params).to_list()

        for document in documents:
            document["id"] = str(document["_id"])
            del document["_id"]

        return [self.document_to_domain(document) for document in documents]

    async def filter_by_tag_name(self, tag_name: str) -> List[Note] | None:
        """Фильтр заметок по тэгу"""
        documents = await self._collection.find({"tags": {"$in": [tag_name]}}).to_list()

        for document in documents:
            document["id"] = str(document["_id"])
            del document["_id"]

        return [self.document_to_domain(document) for document in documents]

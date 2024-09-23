from bson.objectid import ObjectId
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.users.dependencies import Deps
from src.users.errors import UserMongoSchemaNotFound
from src.users.models import UserMongoCreateOrUpdateSchema, UserMongoSchema

router = APIRouter()


@router.post("/users", response_model=UserMongoSchema, tags=["users"])
async def create_user(user_request: UserMongoCreateOrUpdateSchema) -> JSONResponse:
    service = Deps.get_user_service()
    result = service.create(user_request)
    return JSONResponse(content=result.dict(), status_code=status.HTTP_201_CREATED)


@router.get("/users", response_model=list[UserMongoSchema], tags=["users"])
async def list_users() -> JSONResponse:
    service = Deps.get_user_service()
    result = service.get_all()

    return JSONResponse(content=[item.dict() for item in result], status_code=status.HTTP_200_OK)


@router.get("/users/{user_id}", response_model=UserMongoSchema, tags=["users"])
async def get_users(user_id: str) -> JSONResponse:
    service = Deps.get_user_service()
    try:
        result = service.get(ObjectId(user_id))
    except UserMongoSchemaNotFound as error:
        return JSONResponse(content={"message": str(error)}, status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(content=result.dict(), status_code=status.HTTP_200_OK)


@router.put("/users/{user_id}", response_model=UserMongoSchema, tags=["users"])
async def update_user(user_id: str, user_request: UserMongoCreateOrUpdateSchema) -> JSONResponse:
    service = Deps.get_user_service()
    try:
        result = service.update(user_id, user_request)
    except UserMongoSchemaNotFound as error:
        return JSONResponse(content={"message": str(error)}, status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(content=result.dict(), status_code=status.HTTP_200_OK)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def delete_user(user_id: str) -> JSONResponse:
    service = Deps.get_user_service()
    service.delete(user_id)

    return JSONResponse(content={}, status_code=status.HTTP_204_NO_CONTENT)

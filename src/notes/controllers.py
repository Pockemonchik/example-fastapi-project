import json

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.core.errors import APIErrorMessage
from src.notes.application.dto import CreateNoteDTO, NoteDTO
from src.notes.application.note_service import NoteService
from src.notes.bootstrap import Container

router = APIRouter()


@router.get(
    "/notes/{note_id}",
    response_model=NoteDTO,
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["notes"],
)
@inject
async def get_note(note_id: int, service: NoteService = Depends(Provide[Container.service])) -> JSONResponse:
    result = await service.get_note_by_id(id=note_id)
    return JSONResponse(content=json.loads(result.model_dump_json()), status_code=status.HTTP_200_OK)


@router.post(
    "/notes",
    response_model=NoteDTO,
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["notes"],
)
@inject
async def create_note(
    request: CreateNoteDTO, service: NoteService = Depends(Provide[Container.service])
) -> JSONResponse:
    result = await service.create_note(request)
    return JSONResponse(content=json.loads(result.model_dump_json()), status_code=status.HTTP_201_CREATED)

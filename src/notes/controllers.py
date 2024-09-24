from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from kink import di

from src.core.errors import APIErrorMessage
from src.notes.application.dto import CreateNoteDTO, NoteDTO
from src.notes.application.note_service import NoteService

router = APIRouter()


@router.get(
    "/notes/{note_id}",
    response_model=NoteDTO,
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["notes"],
)
async def get_note(request: CreateNoteDTO, note_id: int, service: NoteService = Depends(lambda: di[NoteService])) -> JSONResponse:
    result = await service.get_one_by_id(id=note_id)
    return JSONResponse(content=result.model_dump(), status_code=status.HTTP_201_CREATED)


@router.post(
    "/notes",
    response_model=NoteDTO,
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["notes"],
)
async def create_note(request: CreateNoteDTO, service: NoteService = Depends(lambda: di[NoteService])) -> JSONResponse:
    result = await service.create(request)
    return JSONResponse(content=result.model_dump(), status_code=status.HTTP_201_CREATED)

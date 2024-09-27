import json
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.core.errors import APIErrorMessage
from src.notes.application.dto import CreateNoteDTO, FilterNoteDTO, NoteDTO, UpdateNoteDTO
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
    "/notes/",
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


@router.put(
    "/notes/{note_id}",
    response_model=NoteDTO,
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["notes"],
)
@inject
async def update_note(
    request: UpdateNoteDTO, note_id: int, service: NoteService = Depends(Provide[Container.service])
) -> JSONResponse:
    result = await service.update_note(id=note_id, input_dto=request)
    return JSONResponse(content=json.loads(result.model_dump_json()), status_code=status.HTTP_201_CREATED)


@router.delete(
    "/notes/{note_id}",
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["notes"],
)
@inject
async def delete_note(note_id: int, service: NoteService = Depends(Provide[Container.service])) -> JSONResponse:
    result = await service.delete_note(id=note_id)
    return JSONResponse(content=(result), status_code=status.HTTP_200_OK)


@router.get(
    "/notes/",
    response_model=List[NoteDTO],
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["notes"],
)
@inject
async def get_all(
    service: NoteService = Depends(
        Provide[Container.service],
    ),
) -> JSONResponse:
    result = await service.get_all()
    json_result = [json.loads(item.model_dump_json()) for item in result]
    return JSONResponse(content=json_result, status_code=status.HTTP_200_OK)


@router.get(
    "/notes/filter/",
    response_model=List[NoteDTO],
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["notes"],
)
@inject
async def get_filtered_notes(
    filter: FilterNoteDTO = Depends(),
    service: NoteService = Depends(
        Provide[Container.service],
    ),
) -> JSONResponse:
    result = await service.get_notes_by_filter(filter.model_dump())
    json_result = [json.loads(item.model_dump_json()) for item in result]
    return JSONResponse(content=json_result, status_code=status.HTTP_200_OK)


@router.get(
    "/notes/by_tag_name/",
    response_model=List[NoteDTO],
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["notes"],
)
@inject
async def get_notes_by_tag_name(
    tag_name: str,
    service: NoteService = Depends(
        Provide[Container.service],
    ),
) -> JSONResponse:
    result = await service.get_notes_by_tag_name(tag_name=tag_name)
    json_result = [json.loads(item.model_dump_json()) for item in result]
    return JSONResponse(content=json_result, status_code=status.HTTP_200_OK)

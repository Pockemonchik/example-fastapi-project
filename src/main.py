from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from src.core.errors import APIErrorMessage, DomainError, RepositoryError, ResourceNotFound
from src.notes.bootstrap import Container
from src.notes.controllers import router as notes_router
from src.users.controllers import router as users_router


def create_app() -> FastAPI:
    container = Container()
    container.config.giphy.api_key.from_env("GIPHY_API_KEY")

    app = FastAPI()
    app.include_router(users_router)
    app.include_router(notes_router)
    return app


app = create_app()


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    error_msg = APIErrorMessage(type=exc.__class__.__name__, message=f"Oops! {exc}")
    return JSONResponse(
        status_code=400,
        content=error_msg.dict(),
    )


@app.exception_handler(ResourceNotFound)
async def resource_not_found_handler(request: Request, exc: ResourceNotFound) -> JSONResponse:
    error_msg = APIErrorMessage(type=exc.__class__.__name__, message=str(exc))
    return JSONResponse(status_code=404, content=error_msg.dict())


@app.exception_handler(RepositoryError)
async def repository_error_handler(request: Request, exc: RepositoryError) -> JSONResponse:
    error_msg = APIErrorMessage(
        type=exc.__class__.__name__, message="Oops! Something went wrong, please try again later..."
    )
    return JSONResponse(
        status_code=500,
        content=error_msg.dict(),
    )


def custom_openapi() -> dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema  # type: ignore

    openapi_schema = get_openapi(
        title="example-fastapi-app",
        version="1.0.0",
        description="",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema

    return app.openapi_schema  # type: ignore


app.openapi = custom_openapi  # type: ignore

if __name__ == "__main__":
    uvicorn.run("src.main:app", reload=True)

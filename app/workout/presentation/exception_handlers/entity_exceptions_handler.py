from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.workout.domains.exceptions.app_base_exception import AppBaseError
from app.workout.domains.exceptions.entity_exceptions import (
    EntityCreationError,
    EntityDeletionError,
    EntityNotFoundError,
    EntityUpdateError,
)


def create_entity_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(AppBaseError)
    async def entity_exception_handler(_: Request, exc: AppBaseError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"detail": exc.message}
        )

    @app.exception_handler(EntityCreationError)
    async def entity_creation_exception_handler(
        _: Request, exc: EntityCreationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )

    @app.exception_handler(EntityDeletionError)
    async def entity_deletion_exception_handler(
        _: Request, exc: EntityDeletionError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"detail": exc.message}
        )

    @app.exception_handler(EntityNotFoundError)
    async def entity_not_found_exception_handler(
        _: Request, exc: EntityNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"detail": exc.message}
        )

    @app.exception_handler(EntityUpdateError)
    async def entity_update_exception_handler(
        _: Request, exc: EntityUpdateError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"detail": exc.message}
        )

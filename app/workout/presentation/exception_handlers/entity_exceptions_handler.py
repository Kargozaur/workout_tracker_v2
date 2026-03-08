from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.workout.domains.exceptions.app_base_exception import AppBaseException
from app.workout.domains.exceptions.entity_exceptions import (
    EntityCreationException,
    EntityDeletionException,
    EntityNotFoundException,
    EntityUpdateException,
)


def create_entity_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(AppBaseException)
    async def entity_exception_handler(
        _: Request, exc: AppBaseException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"detail": exc.message}
        )

    @app.exception_handler(EntityCreationException)
    async def entity_creation_exception_handler(
        _: Request, exc: EntityCreationException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )

    @app.exception_handler(EntityDeletionException)
    async def entity_deletion_exception_handler(
        _: Request, exc: EntityDeletionException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"detail": exc.message}
        )

    @app.exception_handler(EntityNotFoundException)
    async def entity_not_found_exception_handler(
        _: Request, exc: EntityNotFoundException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"detail": exc.message}
        )

    @app.exception_handler(EntityUpdateException)
    async def entity_update_exception_handler(
        _: Request, exc: EntityUpdateException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"detail": exc.message}
        )

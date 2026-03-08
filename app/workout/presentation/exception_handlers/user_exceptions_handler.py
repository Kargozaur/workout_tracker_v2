from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.workout.domains.exceptions.user_exceptions import (
    UserExistsException,
    UserFailedToCreateException,
    UserNotFoundException,
)


def create_user_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(UserExistsException)
    async def user_exists_exception(
        _: Request, exception: UserExistsException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": exception.message},
        )

    @app.exception_handler(UserNotFoundException)
    async def user_not_found_exception(
        _: Request, exception: UserNotFoundException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": exception.message},
        )

    @app.exception_handler(UserFailedToCreateException)
    async def user_exception(
        _: Request, exception: UserFailedToCreateException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": exception.message},
        )

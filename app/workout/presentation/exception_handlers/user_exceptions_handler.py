from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.workout.domains.exceptions.user_exceptions import (
    UserExistsError,
    UserFailedToCreateError,
    UserNotFoundError,
)


def create_user_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(UserExistsError)
    async def user_exists_exception(
        _: Request, exception: UserExistsError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": exception.message},
        )

    @app.exception_handler(UserNotFoundError)
    async def user_not_found_exception(
        _: Request, exception: UserNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": exception.message},
        )

    @app.exception_handler(UserFailedToCreateError)
    async def user_exception(
        _: Request, exception: UserFailedToCreateError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": exception.message},
        )

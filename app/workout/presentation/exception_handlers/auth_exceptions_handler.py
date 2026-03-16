from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.workout.domains.exceptions.auth_exceptions import (
    AuthError,
    TokenExpiredError,
)


def create_auth_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(AuthError)
    async def auth_exception_handler(_: Request, exc: AuthError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"message": exc.message}
        )

    async def token_exception_handler(
        _: Request, exc: TokenExpiredError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"message": exc.message}
        )

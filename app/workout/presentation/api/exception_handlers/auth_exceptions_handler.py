from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.workout.domains.exceptions.auth_exceptions import AuthException


def create_auth_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(AuthException)
    async def auth_exception_handler(
            _: Request, exc: AuthException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"message": exc.message}
        )

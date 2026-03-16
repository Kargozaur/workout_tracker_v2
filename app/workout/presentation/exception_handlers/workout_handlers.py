from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.workout.domains.exceptions.workout_exceptions import (
    WorkoutEndError,
    WorkoutNotFoundError,
    WorkoutStartError,
)


def create_workout_exceptions_handler(app: FastAPI) -> None:
    @app.exception_handler(WorkoutEndError)
    async def workout_end_exception_handler(
        _: Request, exc: WorkoutEndError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"message": exc.message}
        )

    @app.exception_handler(WorkoutNotFoundError)
    async def workout_nit_found_exception_handler(
        _: Request, exc: WorkoutNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"message": exc.message}
        )

    @app.exception_handler(WorkoutStartError)
    async def workout_start_exception_handler(
        _: Request, exc: WorkoutStartError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"message": exc.message}
        )

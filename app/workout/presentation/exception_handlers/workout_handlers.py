from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.workout.domains.exceptions.workout_exceptions import (
    WorkoutEndException,
    WorkoutNotFoundException,
    WorkoutStartException,
)


def create_workout_exceptions_handler(app: FastAPI) -> None:
    @app.exception_handler(WorkoutEndException)
    async def workout_end_exception_handler(
        _: Request, exc: WorkoutEndException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"message": exc.message}
        )

    @app.exception_handler(WorkoutNotFoundException)
    async def workout_nit_found_exception_handler(
        _: Request, exc: WorkoutNotFoundException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"message": exc.message}
        )

    @app.exception_handler(WorkoutStartException)
    async def workout_start_exception_handler(
        _: Request, exc: WorkoutStartException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"message": exc.message}
        )

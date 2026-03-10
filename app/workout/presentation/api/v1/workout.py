from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from app.workout.application.common.status_codes import success_status_codes
from app.workout.application.workouts.commands.schedule_workout import (
    CreateWorkoutInteractor,
)
from app.workout.application.workouts.queries.get_all_workouts import (
    GetAllWorkouts,
)
from app.workout.domains.entities.workout_schema import CreateWorkout
from app.workout.presentation.api.annotated.oauth import OAuth2
from app.workout.presentation.schemas.workout_schemas import WorkoutResponse


def create_workout_router() -> APIRouter:
    router = APIRouter(prefix="/workout", tags=["Workout"])

    @router.post(
        "/create_workout",
        status_code=success_status_codes.success,
        response_model=WorkoutResponse,
    )
    @inject
    async def create_workout(
        _: OAuth2,
        interactor: FromDishka[CreateWorkoutInteractor],
        workout_data: CreateWorkout,
    ):
        return await interactor.execute(workout_data)

    @router.get(
        "/workouts",
        status_code=success_status_codes.ok,
        response_model=list[WorkoutResponse],
    )
    @inject
    async def get_all_workouts(
        _: OAuth2, interactor: FromDishka[GetAllWorkouts]
    ):
        return await interactor.execute()

    return router

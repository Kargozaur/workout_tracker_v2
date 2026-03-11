from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from app.workout.application.common.status_codes import success_status_codes
from app.workout.application.workouts.commands.schedule_workout import (
    CreateWorkoutInteractor,
)
from app.workout.application.workouts.commands.start_workout_interactor import (
    StartWorkoutInteractor,
)
from app.workout.application.workouts.queries.get_all_workouts import (
    GetAllWorkouts,
)
from app.workout.application.workouts.queries.get_single_workout import (
    GetSingleWorkout,
)
from app.workout.domains.entities.workout_schema import CreateWorkout
from app.workout.presentation.api.annotated.oauth import OAuth2
from app.workout.presentation.api.annotated.pagination import (
    PaginationAnnotated,
)
from app.workout.presentation.schemas.pagination_schema import (
    PaginatedResponse,
)
from app.workout.presentation.schemas.workout_schemas import WorkoutResponse


def create_workout_router() -> APIRouter:
    router = APIRouter(prefix="/workout", tags=["Workout"])

    @router.post(
        "/create_workout",
        status_code=success_status_codes.success,
        response_model=WorkoutResponse,
        description="Create a new workout.",
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
        response_model=PaginatedResponse[WorkoutResponse],
        description="Get a slice of the workouts.",
    )
    @inject
    async def get_all_workouts(
        _: OAuth2,
        interactor: FromDishka[GetAllWorkouts],
        pagination: PaginationAnnotated,
    ):
        return await interactor.execute(pagination.page, pagination.size)

    @router.get(
        "/workouts/{workout_id}",
        status_code=success_status_codes.ok,
        response_model=WorkoutResponse,
        description="get a single workout by its ID.",
    )
    @inject
    async def get_single_workout(
        _: OAuth2, workout_id: UUID, interactor: FromDishka[GetSingleWorkout]
    ):
        return await interactor.execute(workout_id)

    @router.patch(
        "/workouts/{workout_id}", status_code=success_status_codes.ok
    )
    @inject
    async def start_workout(
        _: OAuth2,
        workout_id: UUID,
        interactor: FromDishka[StartWorkoutInteractor],
    ) -> dict[str, str]:
        return await interactor.execute(workout_id)

    return router

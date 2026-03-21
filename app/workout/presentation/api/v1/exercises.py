from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from app.workout.application.common.dataclasses.pagination import Slice
from app.workout.application.common.status_codes import success_status_codes
from app.workout.application.exercises.queries.get_exercises import GetExercises
from app.workout.presentation.api.annotated.oauth import OAuth2
from app.workout.presentation.api.annotated.pagination import PaginationAnnotated
from app.workout.presentation.schemas.exercise_schema import ExerciseResponse
from app.workout.presentation.schemas.pagination_schema import PaginatedResponse


def create_exercise_router() -> APIRouter:
    router = APIRouter(prefix="/exercises", tags=["Exercises"])

    @router.get(
        "/",
        response_model=PaginatedResponse[ExerciseResponse],
        status_code=success_status_codes.ok,
    )
    @inject
    async def get_exercises(
        _: OAuth2, pag: PaginationAnnotated, interactor: FromDishka[GetExercises]
    ) -> Slice:
        return await interactor.execute(page=pag.page, size=pag.size)

    return router

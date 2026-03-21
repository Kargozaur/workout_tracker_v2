from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Body

from app.workout.application.common.status_codes import success_status_codes
from app.workout.application.workouts.commands.add_item import AddItemInteractor
from app.workout.domains.entities.workout_items_schema import WorkoutItems
from app.workout.presentation.api.annotated.oauth import OAuth2


e_name = Annotated[str, Body(min_length=1)]


def create_items_router() -> APIRouter:
    router = APIRouter(
        prefix="/workout/workouts/{workout_id}", tags=["Items", "Workout"]
    )

    @router.post("/add_item", status_code=success_status_codes.success)
    @inject
    async def add_item(
        _: OAuth2,
        workout_id: UUID,
        exercise_name: e_name,
        data: WorkoutItems,
        interactor: FromDishka[AddItemInteractor],
    ) -> dict:
        return await interactor.execute(workout_id, exercise_name, data)

    return router

from typing import Any
from uuid import UUID

from app.workout.application.common.types.token_types import AccessToken
from app.workout.domains.entities.workout_items_schema import (
    WorkoutItems,
    WorkoutItemsDB,
)
from app.workout.domains.protocols.auth_protocols.itoken import ITokenProvider
from app.workout.domains.protocols.uow_protocol.iuow import IUnitOfWork


class AddItemInteractor:
    def __init__(
        self,
        uow: IUnitOfWork,
        access_token: AccessToken,
        token_provider: ITokenProvider,
    ) -> None:
        self.UoW = uow
        self.access_token = access_token
        self.token_provider = token_provider

    async def execute(
        self, workout_id: UUID, exercise_name: str, data: WorkoutItems
    ) -> dict:
        _: dict[str, Any] = self.token_provider.decode_token(self.access_token)
        exercise = await self.UoW.exercise_repository.get_like(exercise_name)
        if not exercise:
            return {"Failed": f"Exercise with name {exercise_name} doesn't exists"}
        db_data: WorkoutItemsDB = WorkoutItemsDB(
            **data.model_dump(), workoud_id=workout_id, exercise_id=exercise.id
        )
        async with self.UoW:
            await self.UoW.workout_items_repository.create_item(db_data)
            await self.UoW.commit()

        return {"Success": "Added exercise to your workout"}

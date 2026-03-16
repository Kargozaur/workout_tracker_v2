from typing import Any
from uuid import UUID

from app.workout.application.common.types.token_types import AccessToken
from app.workout.domains.entities.workout_schema import (
    CreateWorkout,
    CreateWorkoutDB,
)
from app.workout.domains.protocols.auth_protocols.itoken import ITokenProvider
from app.workout.domains.protocols.uow_protocol.iuow import IUnitOfWork


class CreateWorkoutInteractor:
    def __init__(
        self,
        uow: IUnitOfWork,
        token_provider: ITokenProvider,
        access_token: AccessToken,
    ) -> None:
        self.UoW = uow
        self.token_provider = token_provider
        self.access_token = access_token

    async def execute[T](self, workout: CreateWorkout) -> T:
        user_data: dict[str, Any] = self.token_provider.decode_token(self.access_token)
        user_id: UUID = UUID(user_data.get("sub"))
        schema: CreateWorkoutDB = CreateWorkoutDB(
            user_id=user_id, **workout.model_dump()
        )

        async with self.UoW:
            result: T = await self.UoW.workout_repository.create_workout(schema)
            await self.UoW.commit()

        return result

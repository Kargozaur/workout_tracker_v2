from typing import Any
from uuid import UUID

from app.workout.application.common.types.token_types import AccessToken
from app.workout.domains.protocols.auth_protocols.itoken import ITokenProvider
from app.workout.domains.protocols.uow_protocol.iuow import IUnitOfWork


class GetSingleWorkout:
    def __init__(
        self,
        uow: IUnitOfWork,
        token_provider: ITokenProvider,
        access_token: AccessToken,
    ) -> None:
        self.UoW = uow
        self.token_provider = token_provider
        self.access_token = access_token

    async def execute(self, workout_id: UUID):  # noqa: ANN201
        user_data: dict[str, Any] = self.token_provider.decode_token(self.access_token)
        user_id: UUID = UUID(user_data.get("sub"))
        return await self.UoW.workout_repository.get_workout(
            user_id=user_id, workout_id=workout_id
        )

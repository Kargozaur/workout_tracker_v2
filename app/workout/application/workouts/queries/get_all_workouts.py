from typing import Any
from uuid import UUID

from app.workout.application.common.types.token_types import AccessToken
from app.workout.domains.protocols.auth_protocols.itoken import ITokenProvider
from app.workout.domains.protocols.uow_protocol.iuow import IUnitOfWork


class GetAllWorkouts:
    def __init__(
        self,
        uow: IUnitOfWork,
        token_provider: ITokenProvider,
        access_token: AccessToken,
    ):
        self.UoW = uow
        self.token_provider = token_provider
        self.access_token = access_token

    async def execute(self):
        user_data: dict[str, Any] = self.token_provider.decode_token(
            self.access_token
        )
        user_id: UUID = UUID(user_data.get("sub"))
        return await self.UoW.workout_repository.get_all_workouts(user_id)

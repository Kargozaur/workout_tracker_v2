from typing import Any
from uuid import UUID

from app.workout.application.common.dataclasses.pagination import Slice
from app.workout.application.common.types.token_types import AccessToken
from app.workout.domains.protocols.auth_protocols.itoken import ITokenProvider
from app.workout.domains.protocols.uow_protocol.iuow import IUnitOfWork


class GetAllWorkouts[T]:
    def __init__(
        self,
        uow: IUnitOfWork,
        token_provider: ITokenProvider,
        access_token: AccessToken,
    ) -> None:
        self.UoW = uow
        self.token_provider = token_provider
        self.access_token = access_token

    async def execute(self, page: int, size: int) -> Slice[T]:
        user_data: dict[str, Any] = self.token_provider.decode_token(
            self.access_token
        )
        user_id: UUID = UUID(user_data.get("sub"))
        limit = min(size, 20)
        return await self.UoW.workout_repository.get_all_workouts(
            page, limit, user_id
        )

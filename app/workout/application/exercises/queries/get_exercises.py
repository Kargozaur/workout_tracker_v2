from typing import Any

from app.workout.application.common.dataclasses.pagination import Slice
from app.workout.application.common.types.token_types import AccessToken
from app.workout.domains.protocols.auth_protocols.itoken import ITokenProvider
from app.workout.domains.protocols.uow_protocol.iuow import IUnitOfWork


class GetExercises:
    def __init__(
        self,
        uow: IUnitOfWork,
        acccess_token: AccessToken,
        token_provider: ITokenProvider,
    ) -> None:
        self.UoW = uow
        self.access_token = acccess_token
        self.token_provider = token_provider

    async def execute(self, page: int, size: int) -> Slice:
        _: dict[str, Any] = self.token_provider.decode_token(self.access_token)
        return await self.UoW.exercise_repository.get_exercises(page, size)

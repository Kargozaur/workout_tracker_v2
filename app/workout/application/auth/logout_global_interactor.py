from typing import Any
from uuid import UUID

from app.workout.application.common.transactional import transactional
from app.workout.application.common.types.token_types import (
    AccessToken,
)
from app.workout.domains.protocols.itoken import ITokenProvider
from app.workout.domains.protocols.iuow import IUnitOfWork


class LogoutGlobalInteractor:
    def __init__(
            self,
            uow: IUnitOfWork,
            token_provider: ITokenProvider,
            access_token: AccessToken,
    ) -> None:
        self.UoW = uow
        self.token_provider = token_provider
        self.access_token = access_token

    @transactional
    async def execute(self) -> None:
        user_data: dict[str, Any] = self.token_provider.decode_token(
            self.access_token
        )
        user_id: str = user_data.get("sub")
        await self.UoW.refresh_repository.revoke_refresh_token(
            user_id=UUID(user_id)
        )

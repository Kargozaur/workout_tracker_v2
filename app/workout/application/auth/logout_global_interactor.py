from typing import Any
from uuid import UUID

from loguru import logger

from app.workout.application.common.transactional import transactional
from app.workout.application.common.types.token_types import (
    AccessToken,
)
from app.workout.domains.protocols.icacheservice import ICacheService
from app.workout.domains.protocols.itoken import ITokenProvider
from app.workout.domains.protocols.iuow import IUnitOfWork


class LogoutGlobalInteractor:
    def __init__(
        self,
        uow: IUnitOfWork,
        token_provider: ITokenProvider,
        access_token: AccessToken,
        cache_service: ICacheService,
    ) -> None:
        self.UoW = uow
        self.token_provider = token_provider
        self.access_token = access_token
        self.cache_service = cache_service

    @transactional
    async def execute(self) -> None:
        user_data: dict[str, Any] = self.token_provider.decode_token(
            self.access_token
        )
        user_id: UUID = UUID(user_data.get("sub"))
        logger.debug(f"Found user id in token: {user_id}")
        await self.UoW.refresh_repository.revoke_refresh_token(user_id=user_id)
        await self.cache_service.delete_cache(user_id)
        logger.debug(f"Revoked all tokens: {user_id}")

from typing import Any
from uuid import UUID

from loguru import logger

from app.workout.application.common.transactional import transactional
from app.workout.application.common.types.token_types import RefreshToken
from app.workout.domains.entities.user_schemas import GetUser
from app.workout.domains.protocols.icacheservice import ICacheService
from app.workout.domains.protocols.itoken import ITokenProvider
from app.workout.domains.protocols.itokenhasher import ITokenHasher
from app.workout.domains.protocols.iuow import IUnitOfWork


class LogoutInteractor:
    def __init__(
        self,
        uow: IUnitOfWork,
        token_hasher: ITokenHasher,
        refresh_token: RefreshToken,
        token_provider: ITokenProvider,
        cache_service: ICacheService[GetUser],
    ):
        self.UoW = uow
        self.token_hasher = token_hasher
        self.refresh_token = refresh_token
        self.token_provider = token_provider
        self.cache_service = cache_service

    @transactional
    async def execute(self) -> None:
        token_hash: str = self.token_hasher.hash(self.refresh_token)
        await self.UoW.refresh_repository.revoke_refresh_token(
            token_hash=token_hash
        )
        user_data: dict[str, Any] = self.token_provider.decode_token(
            self.refresh_token
        )
        user_id: str = user_data.get("sub")
        logger.debug(f"User ID: {user_id}")
        await self.cache_service.delete_cache(UUID(user_id))
        logger.debug(f"Deleted all tokens for: {user_id}")

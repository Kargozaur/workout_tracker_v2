from typing import Any
from uuid import UUID

from loguru import logger
from pydantic import BaseModel

from app.workout.application.auth.queries.get_current_user_interactor import (
    GetUserInteractor,
)
from app.workout.application.common.generic_protocols.user_types import (
    CacheUser,
)
from app.workout.application.common.types.token_types import AccessToken
from app.workout.domains.entities.user_schemas import GetUser
from app.workout.domains.protocols.icacheservice import ICacheService
from app.workout.domains.protocols.itoken import ITokenProvider
from app.workout.domains.protocols.iuow import IUnitOfWork


class CachedUserInteractor[T: CacheUser, R: BaseModel](GetUserInteractor):
    """Cached wrapper over GetUserInteractor.
    Transactions are managed inside GetUserInteractor."""

    def __init__(
        self,
        interactor: GetUserInteractor[T],
        token_provider: ITokenProvider,
        service: ICacheService[R],
        access_token: AccessToken,
        uow: IUnitOfWork,
    ) -> None:
        super().__init__(uow, access_token, token_provider)
        self.interactor = interactor
        self.service = service

    async def execute(self) -> T:
        decoded: dict[str, Any] = self.token_provider.decode_token(
            self.access_token
        )
        user_id: UUID = UUID(decoded.get("sub"))
        cached_user: T | None = await self.service.get_cache(user_id)
        if cached_user:
            logger.debug(f"Cache hit: {cached_user}")
            return cached_user
        user_data: T = await self.interactor.execute()
        cached_data: R = GetUser(
            **user_data.__dict__
        )  # passes ORM attributes inside a pydantic model
        await self.service.set_cache(user_id, cached_data)
        logger.debug("Set cache.")
        return user_data

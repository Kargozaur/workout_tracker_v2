from typing import Any
from uuid import UUID

from pydantic import BaseModel

from app.workout.application.common.generic_protocols.user_types import (
    ExistingUser,
)
from app.workout.application.common.types.token_types import AccessToken
from app.workout.domains.entities.user_schemas import GetUser
from app.workout.domains.protocols.auth_protocols.itoken import ITokenProvider
from app.workout.domains.protocols.service_protocols.icacheservice import (
    ICacheService,
)
from app.workout.domains.protocols.uow_protocol.iuow import IUnitOfWork


class UpdateProfileInteractor[T: BaseModel]:
    def __init__(
        self,
        uow: IUnitOfWork,
        token_provider: ITokenProvider,
        cache_service: ICacheService,
        access_token: AccessToken,
    ) -> None:
        self.UoW = uow
        self.token_provider = token_provider
        self.cache_service = cache_service
        self.access_token = access_token

    async def execute(self, update_schema: T) -> ExistingUser:
        payload: dict[str, Any] = self.token_provider.decode_token(
            self.access_token
        )
        user_id: UUID = UUID(payload.get("sub"))
        async with self.UoW:
            user: ExistingUser = await self.UoW.user_repository.update_user(
                update_schema, id=user_id
            )
            await self.UoW.commit()
        cached_user: GetUser = GetUser(**user.__dict__)
        await self.cache_service.delete_cache(user_id)
        await self.cache_service.set_cache(user_id, cached_user)
        return user

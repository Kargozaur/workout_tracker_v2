import datetime as dt
from typing import Any
from uuid import UUID

from loguru import logger

from app.workout.application.common.generic_protocols.refresh_token import (
    RefreshTokenT,
)
from app.workout.application.common.types.token_types import RefreshToken
from app.workout.domains.entities.refresh_token_schema import (
    RefreshTokenSchema,
)
from app.workout.domains.exceptions.auth_exceptions import (
    TokenExpiredException,
)
from app.workout.domains.protocols.auth_protocols.itoken import ITokenProvider
from app.workout.domains.protocols.auth_protocols.itokenhasher import (
    ITokenHasher,
)
from app.workout.domains.protocols.uow_protocol.iuow import IUnitOfWork


class RefreshTokenInteractor[T: RefreshTokenT]:
    def __init__(
        self,
        uow: IUnitOfWork,
        token_provider: ITokenProvider,
        token_hasher: ITokenHasher,
        refresh_token: RefreshToken,
    ) -> None:
        self.UoW = uow
        self.token_provider = token_provider
        self.token_hasher = token_hasher
        self.refresh_token = refresh_token

    async def execute(self) -> tuple[str, str]:
        payload: dict[str, Any] = self.token_provider.decode_token(
            self.refresh_token
        )

        user_id: UUID = UUID(payload.get("sub"))
        exp: int = payload.get("exp")
        current_token_hash: str = self.token_hasher.hash(self.refresh_token)

        db_token: (
            T | None
        ) = await self.UoW.refresh_repository.get_refresh_token(
            token_hash=current_token_hash,
            fields=("id", "token_hash"),
        )
        if not db_token:
            raise TokenExpiredException("Token nod found")

        exp_dt: dt.datetime = dt.datetime.fromtimestamp(exp, tz=dt.UTC)
        now: dt.datetime = dt.datetime.now(dt.UTC)
        if exp_dt < now:
            raise TokenExpiredException("Token expired")

        left: dt.timedelta = exp_dt - dt.datetime.now(dt.UTC)
        new_refresh_token: str | None = None
        if left < dt.timedelta(days=1):
            new_refresh_token: str = self.token_provider.create_refresh_token(
                user_id
            )
            token_hash: str = self.token_hasher.hash(new_refresh_token)
            token_schema: RefreshTokenSchema = RefreshTokenSchema(
                user_id=user_id, token_hash=token_hash
            )
            async with self.UoW:
                logger.debug("Entered refresh context")
                await self.UoW.refresh_repository.revoke_refresh_token(
                    token_hash=current_token_hash
                )
                await self.UoW.refresh_repository.create_refresh_token(
                    token_schema
                )
                await self.UoW.commit()
            logger.debug("Updated token")
        access_token: str = self.token_provider.create_access_token(user_id)
        return access_token, new_refresh_token or self.refresh_token

import asyncio

from loguru import logger

from app.workout.application.common.generic_protocols.user_types import (
    ExistingUser,
)
from app.workout.domains.entities.refresh_token_schema import (
    RefreshTokenSchema,
)
from app.workout.domains.entities.user_schemas import LoginSchema
from app.workout.domains.exceptions.user_exceptions import (
    UserNotFoundError,
)
from app.workout.domains.protocols.auth_protocols.ihasher import (
    IPasswordHasher,
)
from app.workout.domains.protocols.auth_protocols.itoken import ITokenProvider
from app.workout.domains.protocols.auth_protocols.itokenhasher import (
    ITokenHasher,
)
from app.workout.domains.protocols.uow_protocol.iuow import IUnitOfWork


class LoginInteractor[T: ExistingUser]:
    def __init__(
        self,
        uow: IUnitOfWork,
        token_provider: ITokenProvider,
        token_hasher: ITokenHasher,
        password_hasher: IPasswordHasher,
    ) -> None:
        self.UoW = uow
        self.token_provider = token_provider
        self.token_hasher = token_hasher
        self.password_hasher = password_hasher

    async def execute(self, login: LoginSchema) -> tuple[str, str]:
        user: T | None = await self.UoW.user_repository.get_user(
            email=login.email, fields=("id", "email", "password_hash")
        )
        if not user:
            raise UserNotFoundError("User with such email does not exist")
        is_correct_password: bool = await asyncio.to_thread(
            self.password_hasher.verify_password,
            login.password,
            user.password_hash,
        )
        if not is_correct_password:
            raise UserNotFoundError("User with such email does not exist")

        access_token: str = self.token_provider.create_access_token(user.id)
        refresh_token: str = self.token_provider.create_refresh_token(user.id)
        refresh_token_hash: str = self.token_hasher.hash(refresh_token)
        refresh_schema: RefreshTokenSchema = RefreshTokenSchema(
            user_id=user.id, token_hash=refresh_token_hash
        )
        async with self.UoW:
            await self.UoW.refresh_repository.create_refresh_token(refresh_schema)
            await self.UoW.commit()
        logger.debug(f"Access: {access_token[:-5]}. Refresh: {refresh_token[:-5]}")

        return access_token, refresh_token

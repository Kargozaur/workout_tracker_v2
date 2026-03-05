import anyio

from app.workout.application.common.transactional import transactional
from app.workout.domains.entities.refresh_token_schema import (
    RefreshTokenSchema,
)
from app.workout.domains.entities.user_schemas import LoginSchema
from app.workout.domains.exceptions.user_exceptions import (
    UserNotFoundException,
)
from app.workout.domains.protocols.ihasher import IPasswordHasher
from app.workout.domains.protocols.itoken import ITokenProvider
from app.workout.domains.protocols.itokenhasher import ITokenHasher
from app.workout.domains.protocols.iuow import IUnitOfWork


class LoginInteractor:
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

    @transactional
    async def execute[UserEntity](self, login: LoginSchema) -> tuple[str, str]:
        user: UserEntity | None = await self.UoW.user_repository.get_user(
            email=login.email, fields=("id", "email", "password_hash")
        )
        if not user:
            raise UserNotFoundException("User with such email does not exist")
        is_correct_password: bool = await anyio.to_thread.run_sync(
            self.password_hasher.verify_password,
            login.password,
            user.password_hash,
        )
        if not is_correct_password:
            raise UserNotFoundException("User with such email does not exist")

        access_token: str = await self.token_provider.create_access_token(
            user.id
        )
        refresh_token: str = await self.token_provider.create_refresh_token(
            user.id
        )
        refresh_token_hash: str = self.token_hasher.hash(refresh_token)
        refresh_schema: RefreshTokenSchema = RefreshTokenSchema(
            user_id=user.id, token_hash=refresh_token_hash
        )
        await self.UoW.refresh_repository.revoke_refresh_token(user_id=user.id)
        await self.UoW.refresh_repository.create_refresh_token(refresh_schema)
        return access_token, refresh_token

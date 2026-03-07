import anyio

from app.workout.application.common.generic_protocols.user_types import (
    NotExistingUser,
)
from app.workout.application.common.transactional import transactional
from app.workout.domains.entities.user_schemas import CreateUser
from app.workout.domains.exceptions.user_exceptions import (
    UserExistsException,
)
from app.workout.domains.protocols.ihasher import IPasswordHasher
from app.workout.domains.protocols.iuow import IUnitOfWork


class RegisterUser[T: NotExistingUser]:
    def __init__(self, uow: IUnitOfWork, hasher: IPasswordHasher) -> None:
        self.UoW = uow
        self.hasher = hasher

    @transactional
    async def execute(self, user_data: CreateUser) -> T:
        existing_user: T | None = await self.UoW.user_repository.get_user(
            email=user_data.email
        )
        if existing_user:
            raise UserExistsException("Failed to create user")
        hashed_password: str = await anyio.to_thread.run_sync(
            self.hasher.hash_password, user_data.password
        )
        user_data.password = hashed_password
        user: T = await self.UoW.user_repository.create_user(user_data)
        return user

import anyio

from app.workout.application.common.transactional import transactional
from app.workout.domains.entities.user_schemas import CreateUser
from app.workout.domains.exceptions.user_exceptions import (
    UserExistsException,
)
from app.workout.domains.protocols.ihasher import IPasswordHasher
from app.workout.domains.protocols.iuow import IUnitOfWork


class RegisterUser[UserEntity]:
    def __init__(self, uow: IUnitOfWork, hasher: IPasswordHasher) -> None:
        self.UoW = uow
        self.hasher = hasher

    @transactional
    async def execute(self, user_data: CreateUser) -> UserEntity:
        existing_user: (
                UserEntity | None
        ) = await self.UoW.user_repository.get_user(email=user_data.email)
        if existing_user:
            raise UserExistsException("Failed to create user")
        hashed_password: str = await anyio.to_thread.run_sync(
            self.hasher.hash_password, user_data.password
        )
        user_data.password = hashed_password
        user: UserEntity = await self.UoW.user_repository.create_user(
            user_data
        )
        return user

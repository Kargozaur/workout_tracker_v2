from app.workout.domains.entities.user_schemas import CreateUser, UpdateUser
from app.workout.domains.protocols.iuser_repository import IUserRepository
from app.workout.infrastructure.db.models.user import User

from . import AsyncSession, BaseRepository


class UserRepository(
    IUserRepository[User, CreateUser, UpdateUser],
    BaseRepository[User, CreateUser, UpdateUser],
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def get_user(self, **filters: object) -> User:
        return await super().get_entity(**filters)

    async def create_user(self, attributes: CreateUser) -> User:
        return await super().create_entity(attributes)

    async def update_user(
            self, attributes: UpdateUser, **filters: object
    ) -> User:
        return await super().update_entity(attributes, **filters)

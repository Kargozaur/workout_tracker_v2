from abc import abstractmethod

from app.workout.domains.protocols.repository_protocols.irepository import (
    IRepository,
)

from . import (
    BaseModel,
)


class IUserRepository[
    UserModelT,
    CreateUserSchemaT: BaseModel,
    UpdateUserSchemaT: BaseModel | None = None,
](IRepository[UserModelT, CreateUserSchemaT, UpdateUserSchemaT]):
    @abstractmethod
    async def create_user(self, schema: CreateUserSchemaT) -> UserModelT: ...

    @abstractmethod
    async def get_user(self, **filters: object) -> UserModelT: ...

    @abstractmethod
    async def update_user(
        self, attributes: UpdateUserSchemaT, **filters: object
    ) -> UserModelT: ...

from abc import abstractmethod

from . import BaseModel, Protocol


class IUserRepository[
    UserModelT,
    CreateUserSchemaT: BaseModel,
    UpdateUserSchemaT: BaseModel | None = None,
](Protocol):
    @abstractmethod
    async def create_user(self, schema: CreateUserSchemaT) -> UserModelT: ...

    @abstractmethod
    async def get_user(self, **filters: object) -> UserModelT: ...

    @abstractmethod
    async def update_user(
        self, attributes: UpdateUserSchemaT, **filters: object
    ) -> UserModelT: ...

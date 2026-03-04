from . import BaseModel, IRepository, abstractmethod


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
        self, attributes: UpdateUserSchemaT | object
    ) -> UserModelT: ...

    @abstractmethod
    async def delete_user(self, **filters: object) -> bool: ...

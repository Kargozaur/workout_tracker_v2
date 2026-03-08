from abc import abstractmethod

from app.workout.domains.protocols.auth_protocols import BaseModel, Protocol


class IRefreshRepository[
    ModelT,
    CreateSchemaT: BaseModel,
](Protocol):
    @abstractmethod
    async def get_refresh_token(self, **filters) -> ModelT: ...

    @abstractmethod
    async def create_refresh_token(
        self, create_schema: CreateSchemaT
    ) -> ModelT: ...

    @abstractmethod
    async def revoke_refresh_token(self, **filters) -> bool: ...

    @abstractmethod
    async def delete_expired(self) -> bool: ...

    @abstractmethod
    async def bulk_delete_refresh_token(self, **filters) -> bool: ...

from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from pydantic import BaseModel


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

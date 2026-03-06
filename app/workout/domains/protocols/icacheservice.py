from abc import abstractmethod
from uuid import UUID

from pydantic import BaseModel

from . import Protocol


class ICacheService[R: BaseModel, T: bytes | None](Protocol):
    @abstractmethod
    async def get_cache(self, user_id: UUID) -> R: ...

    @abstractmethod
    async def set_cache(self, user_id: UUID, cache_attributes: R) -> None: ...

    @abstractmethod
    async def delete_cache(self, user_id: UUID) -> None: ...

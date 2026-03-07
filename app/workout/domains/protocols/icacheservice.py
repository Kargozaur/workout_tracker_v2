from abc import abstractmethod

from pydantic import BaseModel

from . import Protocol


class ICacheService[R: BaseModel](Protocol):
    @abstractmethod
    async def get_cache(self, identifier: object) -> R: ...

    @abstractmethod
    async def set_cache(
        self, identifier: object, cache_attributes: R
    ) -> None: ...

    @abstractmethod
    async def delete_cache(self, identifier: object) -> None: ...

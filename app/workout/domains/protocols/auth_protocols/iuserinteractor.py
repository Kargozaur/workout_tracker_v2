from abc import abstractmethod

from . import Protocol


class IUserInteractor(Protocol):
    @abstractmethod
    async def execute(self): ...

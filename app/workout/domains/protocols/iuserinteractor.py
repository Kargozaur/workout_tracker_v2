from abc import abstractmethod
from typing import Protocol


class IUserInteractor(Protocol):
    @abstractmethod
    async def execute(self): ...

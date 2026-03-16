from abc import abstractmethod
from typing import Protocol

from pydantic import BaseModel


class IExerciseRepository[ModelT, T: BaseModel](Protocol):
    @abstractmethod
    async def create_exercises(self, exercises: list[T]) -> None: ...

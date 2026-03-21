from abc import abstractmethod
from typing import Protocol

from pydantic import BaseModel

from app.workout.application.common.dataclasses.pagination import Slice


class IExerciseRepository[ModelT, T: BaseModel](Protocol):
    @abstractmethod
    async def create_exercises(self, exercises: list[T]) -> int: ...

    @abstractmethod
    async def get_like(self, exercise_name: str) -> ModelT | None: ...

    @abstractmethod
    async def get_exercises(self, page: int, size: int) -> Slice[ModelT]: ...

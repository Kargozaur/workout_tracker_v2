from abc import abstractmethod
from uuid import UUID

from . import BaseModel, Protocol


class IWorkoutRepository[
    ModelT,
    CreateSchemaT: BaseModel,
    UpdateSchemaT: BaseModel,
](Protocol):
    @abstractmethod
    async def create_workout(self, schema: CreateSchemaT) -> ModelT: ...

    @abstractmethod
    async def get_workout(self, **filters: object) -> ModelT: ...

    @abstractmethod
    async def start_workout(self, user_id: UUID, workout_id: UUID) -> bool: ...

    @abstractmethod
    async def cancel_workout(
        self, user_id: UUID, workout_id: UUID
    ) -> bool: ...

    @abstractmethod
    async def finish_workout(self, **filters: object) -> bool: ...

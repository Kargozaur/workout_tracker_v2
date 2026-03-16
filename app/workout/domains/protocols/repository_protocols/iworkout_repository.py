from abc import abstractmethod
from uuid import UUID

from app.workout.application.common.dataclasses.pagination import Slice
from app.workout.domains.entities.workout_schema import AddNote

from . import BaseModel, Protocol


class IWorkoutRepository[
    ModelT,
    CreateSchemaT: BaseModel,
    UpdateSchemaT: BaseModel,
](Protocol):
    @abstractmethod
    async def get_all_workouts(
        self, page: int, size: int, user_id: UUID
    ) -> Slice[ModelT]: ...

    @abstractmethod
    async def create_workout(self, schema: CreateSchemaT) -> ModelT: ...

    @abstractmethod
    async def get_workout(self, user_id: UUID, workout_id: UUID) -> ModelT | None: ...

    @abstractmethod
    async def start_workout(self, user_id: UUID, workout_id: UUID) -> ModelT: ...

    @abstractmethod
    async def cancel_workout(self, user_id: UUID, workout_id: UUID) -> ModelT: ...

    @abstractmethod
    async def finish_workout(self, user_id: UUID, workout_id: UUID) -> ModelT: ...

    @abstractmethod
    async def add_note(
        self, note: AddNote, user_id: UUID, workout_id: UUID
    ) -> ModelT | None: ...

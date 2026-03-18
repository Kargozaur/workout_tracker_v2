from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from pydantic import BaseModel


class IWorkoutItems[ModelT, CreateSchemaT: BaseModel, UpdateSchemaT: BaseModel](
    Protocol
):
    @abstractmethod
    async def create_item(self, schema: CreateSchemaT) -> ModelT: ...

    @abstractmethod
    async def update_item(
        self, workout_id: UUID, exercise_id: UUID, schema: UpdateSchemaT
    ) -> ModelT: ...

    @abstractmethod
    async def delete_item(self, workout_id: UUID, exercise_id: UUID) -> None: ...

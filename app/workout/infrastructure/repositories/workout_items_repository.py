from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.workout.domains.entities.workout_items_schema import (
    UpdateWorkoutItems,
    WorkoutItemsDB,
)
from app.workout.domains.protocols.repository_protocols.iworkout_items_repository import (  # noqa: E501
    IWorkoutItems,
)
from app.workout.infrastructure.db.models.workout_items import WorkoutItems
from app.workout.infrastructure.repositories.base_repository import BaseRepository


class WorkoutItemsRepository(
    BaseRepository[WorkoutItems, WorkoutItemsDB, UpdateWorkoutItems],
    IWorkoutItems[WorkoutItems, WorkoutItemsDB, UpdateWorkoutItems],
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, WorkoutItems)

    async def create_item(self, schema: WorkoutItemsDB) -> WorkoutItems:
        return await super().create_entity(schema)

    async def update_item(
        self, workout_id: UUID, exercise_id: UUID, schema: UpdateWorkoutItems
    ) -> WorkoutItems:
        return await super().update_entity(
            schema, workout_id=workout_id, exercise_id=exercise_id
        )

    async def delete_item(self, workout_id: UUID, exercise_id: UUID) -> None:
        await super().delete_entity(workout_id=workout_id, exercise_id=exercise_id)

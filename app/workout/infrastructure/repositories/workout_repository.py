from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.workout.application.common.dataclasses.pagination import Slice
from app.workout.application.common.enums.workout_statuses import (
    WorkoutStatuses,
)
from app.workout.domains.entities.workout_schema import (
    AddNote,
    CancelWorkout,
    CreateWorkout,
    UpdateFinishedAt,
    UpdateStartedAt,
)
from app.workout.domains.exceptions.workout_exceptions import (
    WorkoutEndError,
    WorkoutNotFoundError,
    WorkoutStartError,
)
from app.workout.domains.protocols.repository_protocols.iworkout_repository import (
    IWorkoutRepository,
)
from app.workout.infrastructure.db.models.workouts import Workout
from app.workout.infrastructure.repositories.base_repository import (
    BaseRepository,
)


class WorkoutRepository(
    BaseRepository[
        Workout,
        CreateWorkout,
        UpdateStartedAt | UpdateFinishedAt | AddNote | CancelWorkout,
    ],
    IWorkoutRepository[Workout, CreateWorkout, UpdateStartedAt | UpdateFinishedAt],
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Workout)

    async def get_all_workouts(
        self, page: int, size: int, user_id: UUID
    ) -> Slice[Workout]:
        """Gets slice of workouts.
        fields and order_by may be passed as keyword arguments.
        """
        return await super().get_all_records(
            page=page,
            size=size,
            user_id=user_id,
            fields=(
                "id",
                "name",
                "status",
                "scheduled_at",
                "started_at",
                "finished_at",
                "note",
            ),
            order_by=("-scheduled_at",),
        )

    async def get_workout(self, user_id: UUID, workout_id: UUID) -> Workout | None:
        return await super().get_entity(
            id=workout_id,
            user_id=user_id,
            fields=(
                "id",
                "name",
                "status",
                "scheduled_at",
                "started_at",
                "finished_at",
                "note",
            ),
        )

    async def create_workout(self, schema: CreateWorkout) -> Workout:
        return await super().create_entity(schema)

    async def start_workout(self, user_id: UUID, workout_id: UUID) -> Workout:
        workout: Workout | None = await super().get_entity(
            id=workout_id,
            user_id=user_id,
            fields=(
                "id",
                "name",
                "status",
                "scheduled_at",
                "started_at",
                "finished_at",
                "note",
            ),
        )
        if not workout:
            raise WorkoutNotFoundError()
        if workout.started_at:
            raise WorkoutStartError("Failed to start workout. Workout already started.")
        if workout.finished_at:
            raise WorkoutStartError(
                "Failed to start workout. Workout already finished."
            )
        start: UpdateStartedAt = UpdateStartedAt()
        result = await super().update_entity(start, id=workout.id, user_id=user_id)
        return result

    async def finish_workout(self, user_id: UUID, workout_id: UUID) -> Workout:
        workout: Workout | None = await super().get_entity(
            id=workout_id,
            user_id=user_id,
            fields=("id", "started_at", "finished_at"),
        )
        if not workout:
            raise WorkoutNotFoundError()
        if not workout.started_at:
            raise WorkoutEndError("Failed to finish workout. Workout not started.")
        if workout.finished_at:
            raise WorkoutEndError("Failed to finish workout. Workout already finished.")
        finish: UpdateFinishedAt = UpdateFinishedAt()
        result = await super().update_entity(finish, id=workout.id, user_id=user_id)
        return result

    async def cancel_workout(self, user_id: UUID, workout_id: UUID) -> Workout:
        workout: Workout | None = await super().get_entity(
            id=workout_id,
            user_id=user_id,
            fields=("id", "started_at", "finished_at", "status"),
        )
        if not workout:
            raise WorkoutNotFoundError()

        if workout.status == WorkoutStatuses.CANCELLED:
            raise WorkoutEndError("Workout already cancelled")

        if workout.finished_at:
            raise WorkoutEndError("Failed to cancel workout. Workout already finished.")

        cancel: CancelWorkout = CancelWorkout()
        result = await super().update_entity(cancel, id=workout.id, user_id=user_id)
        return result

    async def add_note(
        self, note: AddNote, user_id: UUID, workout_id: UUID
    ) -> Workout | None:
        return await super().update_entity(
            note,
            id=workout_id,
            user_id=user_id,
            fields=(
                "id",
                "name",
                "status",
                "scheduled_at",
                "started_at",
                "finished_at",
                "note",
            ),
        )

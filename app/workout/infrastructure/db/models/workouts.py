from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.workout.application.common.enums.workout_statuses import (
    WorkoutStatuses,
)

from . import Base, CreatedAtMixin, UUIDIdMixin, date_time_column


class Workout(UUIDIdMixin, CreatedAtMixin, Base):
    __tablename__ = "workouts"

    user_id: Mapped[UUID] = mapped_column(
        sa.ForeignKey("user.id", ondelete="CASCADE"),
    )
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    status: Mapped[WorkoutStatuses] = mapped_column(
        sa.Enum(
            WorkoutStatuses, values_callable=lambda x: [e.value for e in x]
        ),
        nullable=False,
    )
    scheduled_at: Mapped[date_time_column()]
    started_at: Mapped[date_time_column()]
    finished_at: Mapped[date_time_column()]
    note: Mapped[str] = mapped_column(
        sa.String(255), nullable=False, default=""
    )

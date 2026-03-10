import datetime as dt
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.workout.application.common.enums.workout_statuses import (
    WorkoutStatuses,
)

from . import Base, CreatedAtMixin, UUIDIdMixin


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
    scheduled_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=False
    )
    started_at: Mapped[dt.datetime | None] = mapped_column(
        sa.DateTime(timezone=True), nullable=True
    )
    finished_at: Mapped[dt.datetime | None] = mapped_column(
        sa.DateTime(timezone=True), nullable=True
    )
    note: Mapped[str] = mapped_column(
        sa.String(255), nullable=False, default=""
    )

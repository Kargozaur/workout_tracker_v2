import datetime as dt
from typing import Annotated
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.workout.application.common.enums.workout_statuses import (
    WorkoutStatuses,
)

from . import Base, CreatedAtMixin, UUIDIdMixin


def timestamp(nullable: bool = True) -> mapped_column:
    return Annotated[
        dt.datetime,
        mapped_column(
            sa.DateTime(timezone=True),
            nullable=nullable,
            server_default=sa.func.now(),
            default=lambda: dt.datetime.now(dt.UTC),
        ),
    ]


class Workout(UUIDIdMixin, CreatedAtMixin, Base):
    __tablename__ = "workouts"

    user_id: Mapped[UUID] = mapped_column(
        sa.ForeignKey("user.id", ondelete="CASCADE"),
    )
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    status: Mapped[WorkoutStatuses] = mapped_column(
        sa.Enum(WorkoutStatuses), nullable=False
    )
    scheduled_at: Mapped[timestamp()]
    started_at: Mapped[timestamp()]
    finished_at: Mapped[timestamp()]
    note: Mapped[str] = mapped_column(
        sa.String(255), nullable=False, default=""
    )

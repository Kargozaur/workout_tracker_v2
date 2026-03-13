from decimal import Decimal
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from . import Base, UpdatedAtMixin


class WorkoutItems(UpdatedAtMixin, Base):
    __tablename__ = "workout_items"

    workout_id: Mapped[UUID] = mapped_column(
        sa.ForeignKey("workouts.id", ondelete="CASCADE"),
        index=True,
        primary_key=True,
    )
    exercise_id: Mapped[UUID] = mapped_column(
        sa.ForeignKey("exercises.id"),
        index=True,
        primary_key=True,
    )
    order_index: Mapped[Decimal] = mapped_column(
        sa.DECIMAL(precision=4, scale=2)
    )
    is_completed: Mapped[bool] = mapped_column(
        sa.BOOLEAN(), default=False, nullable=False, server_default=sa.false()
    )

    __table_args__ = (
        sa.UniqueConstraint(workout_id, exercise_id, name="workout_items_uc"),
    )

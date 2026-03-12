from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base, UUIDIdMixin


class Exercises(UUIDIdMixin, Base):
    __tablename__ = "exercises"

    name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    description: Mapped[str] = mapped_column(
        sa.String(255), nullable=True, default=""
    )
    reps: Mapped[int] = mapped_column(sa.Integer, nullable=True)
    distance_km: Mapped[Decimal] = mapped_column(
        sa.DECIMAL(precision=5, scale=2), nullable=True
    )
    duration_seconds: Mapped[Decimal] = mapped_column(
        sa.DECIMAL(precision=5, scale=2), nullable=True
    )
    category_id: Mapped[int] = mapped_column(
        sa.ForeignKey("categories.id"), nullable=True
    )
    muscle_group_id: Mapped[int] = mapped_column(
        sa.ForeignKey("muscle_groups.id"), nullable=True
    )

    workout = relationship(
        "Workout",
        back_populates="exercises",
        secondary="workout_items",
        cascade="all, delete-orphan",
    )
    category = relationship("Category", back_populates="exercises")
    muscle_group = relationship("MuscleGroup", back_populates="exercises")

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base, UUIDIdMixin


class Exercises(UUIDIdMixin, Base):
    __tablename__ = "exercises"

    name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    description: Mapped[str] = mapped_column(
        sa.String(500), nullable=True, default=""
    )
    exercise_slug: Mapped[str] = mapped_column(sa.String(100), nullable=True)
    category_id: Mapped[int] = mapped_column(
        sa.ForeignKey("categories.id"), nullable=True
    )
    muscle_group_id: Mapped[int] = mapped_column(
        sa.ForeignKey("muscle_groups.id"), nullable=True
    )
    workout_items = relationship(
        "WorkoutItems", back_populates="items", lazy="selectin"
    )
    category = relationship("Category", back_populates="exercises")
    muscle_groups = relationship("MuscleGroups", back_populates="exercises")

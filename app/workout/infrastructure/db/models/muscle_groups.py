import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.workout.application.common.enums.muscle_groups import (
    MuscleGroups as MuscleGroupEnum,
)

from . import Base, IntIdMixin


class MuscleGroups(IntIdMixin, Base):
    __tablename__ = "muscle_groups"

    groups: Mapped[MuscleGroupEnum] = mapped_column(
        sa.Enum(
            MuscleGroupEnum, values_callable=lambda x: [e.value for e in x]
        )
    )
    exercises = relationship("Exercise", back_populates="muscle_groups")

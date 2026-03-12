import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.workout.application.common.enums.categories import (
    Category as CategoryEnum,
)

from . import Base, IntIdMixin


class Category(IntIdMixin, Base):
    __tablename__ = "categories"

    category: Mapped[CategoryEnum] = sa.Column(
        sa.Enum(CategoryEnum, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )
    exercises = relationship("Exercise", back_populates="category")

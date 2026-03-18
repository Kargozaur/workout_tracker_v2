from decimal import Decimal
from typing import Self
from uuid import UUID

from . import BaseModel, ConfigDict, Field, model_validator


class WorkoutItemsBase(BaseModel):
    order_index: int
    is_completed: bool = Field(default=False)
    reps: int | None = Field(default=None, gt=0)
    distance_km: Decimal | None = Field(
        default=None, max_digits=5, decimal_places=2, gt=0
    )
    duration_seconds: Decimal | None = Field(
        default=None, max_digits=5, decimal_places=2, gt=0
    )


class WorkoutItems(WorkoutItemsBase):
    @model_validator(mode="after")
    def validate(self) -> Self:
        if self.reps and self.distance_km:
            raise ValueError("Only one measure must be provided")
        if not self.reps and not self.distance_km:
            raise ValueError("Either reps or distance must be provided")
        return self


class WorkoutItemsDB(WorkoutItemsBase):
    workoud_id: UUID
    exercise_id: UUID


class UpdateWorkoutItems(WorkoutItems): ...

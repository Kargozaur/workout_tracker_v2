import datetime as dt
from typing import Self
from uuid import UUID

from app.workout.application.common.enums.workout_statuses import (
    WorkoutStatuses,
)

from . import (
    BaseModel,
    Field,
    model_validator,
)


class CreateWorkout(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    status: WorkoutStatuses = Field(default=WorkoutStatuses.SCHEDULED)
    scheduled_at: dt.datetime = Field(
        default_factory=lambda: (
            dt.datetime.now(dt.UTC) + dt.timedelta(hours=24)
        )
    )
    started_at: dt.datetime | None = Field(default=None)
    finished_at: dt.datetime | None = Field(default=None)
    note: str = Field(default="", min_length=1, max_length=255)

    @model_validator(mode="after")
    def validate(self) -> Self:
        if self.finished_at and not self.started_at:
            raise ValueError("You can't finish workout before starting it")

        if self.started_at and self.started_at < self.scheduled_at:
            raise ValueError("You can't schedule workout before now")

        if self.finished_at and self.started_at:
            if self.finished_at < self.started_at:
                raise ValueError("You can't finish workout before starting it")

        return self


class UpdateStartedAt(BaseModel):
    started_at: dt.datetime = Field(
        default_factory=lambda: dt.datetime.now(dt.UTC)
    )


class UpdateFinishedAt(BaseModel):
    finished_at: dt.datetime = Field(
        default_factory=lambda: dt.datetime.now(dt.UTC) + dt.timedelta(hours=1)
    )

class CancelWorkout(BaseModel):
    status: WorkoutStatuses = Field(default=WorkoutStatuses.CANCELLED)
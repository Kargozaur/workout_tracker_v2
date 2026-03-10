import datetime as dt
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, BeforeValidator, ConfigDict


def replace_none(v: str) -> BeforeValidator:
    return BeforeValidator(lambda x: x if x is not None else v)


NotStarted = Annotated[
    str | dt.datetime, replace_none("Workout is not yet started")
]
NotFinished = Annotated[
    str | dt.datetime, replace_none("Workout is not yet finished")
]


class WorkoutResponse(BaseModel):
    id: UUID
    name: str
    status: str
    note: str
    scheduled_at: dt.datetime
    started_at: NotStarted
    finished_at: NotFinished

    model_config = ConfigDict(from_attributes=True)

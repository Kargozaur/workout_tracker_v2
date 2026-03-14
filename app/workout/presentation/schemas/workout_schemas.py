import datetime as dt
from typing import Annotated
from uuid import UUID

from pydantic import BeforeValidator

from . import ConfigDict, Field, GenericId


def replace_none(v: str) -> BeforeValidator:
    return BeforeValidator(lambda x: x if x is not None else v)


NotStarted = Annotated[
    str | dt.datetime, replace_none("Workout is not yet started")
]
NotFinished = Annotated[
    str | dt.datetime, replace_none("Workout is not yet finished")
]


class WorkoutResponse(GenericId[UUID]):
    name: str
    status: str
    note: str
    scheduled_at: dt.datetime = Field(serialization_alias="scheduledAt")
    started_at: NotStarted = Field(serialization_alias="startedAt")
    finished_at: NotFinished = Field(serialization_alias="finishedAt")

    model_config = ConfigDict(from_attributes=True)

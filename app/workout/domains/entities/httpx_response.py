from pydantic.alias_generators import to_camel

from . import BaseModel, ConfigDict, Field


class ResponseBaseSchema(BaseModel):
    model_config = ConfigDict(validate_by_alias=True, alias_generator=to_camel)


class Metadata(ResponseBaseSchema):
    total_exercises: int
    total_pages: int
    current_page: int
    previous_page: str | None
    next_page: str


class Data(ResponseBaseSchema):
    exercise_id: str
    name: str
    target_muscles: list[str]
    body_parts: list[str]
    description: list[str] = Field(serialization_alias="instructions")


class ResponseSchema(ResponseBaseSchema):
    success: bool
    metadata: Metadata
    data: list[Data]

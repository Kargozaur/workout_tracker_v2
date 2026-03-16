from . import BaseModel, ConfigDict, Field


class ExerciseSchema(BaseModel):
    name: str = Field(max_length=100)
    description: str = Field(max_length=500)
    exercise_slug: str
    category_id: int
    muscle_group_id: int

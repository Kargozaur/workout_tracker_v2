from typing import Any

import sqlalchemy as sa
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.workout.domains.entities.exercises_schema import ExerciseSchema
from app.workout.domains.protocols.repository_protocols.iexerciserepository import (
    IExerciseRepository,
)
from app.workout.infrastructure.db.models.exercises import Exercises
from app.workout.infrastructure.repositories.base_repository import BaseRepository


class ExerciseRepository(
    BaseRepository[Exercises, ExerciseSchema, None],
    IExerciseRepository[Exercises, ExerciseSchema],
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Exercises)

    async def create_exercises(self, exercises: list[ExerciseSchema]) -> int:
        return await super().bulk_insert(exercises)

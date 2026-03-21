from typing import Any

import sqlalchemy as sa
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.workout.application.common.dataclasses.pagination import Slice
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

    async def get_exercises(self, page: int, size: int) -> Slice[Exercises]:
        return await super().get_all_records(
            page, size, fields=("name, description, id "), order_by=("name")
        )

    async def get_like(self, exercise_name: str) -> Exercises | None:
        query = sa.select(Exercises).where(
            Exercises.name.ilike(f"%{exercise_name.lower().strip()}%")
        )
        res = await self.session.execute(query)
        return res.scalar_one_or_none()

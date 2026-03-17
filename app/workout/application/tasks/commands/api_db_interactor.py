from collections.abc import AsyncIterable

from loguru import logger

from app.workout.application.common.dataclasses.categories_dc import CategoryToId
from app.workout.application.common.dataclasses.groups_dc import MuscleGroupToId
from app.workout.domains.entities.exercises_schema import ExerciseSchema
from app.workout.domains.entities.httpx_response import ResponseSchema
from app.workout.domains.protocols.uow_protocol.iuow import IUnitOfWork
from app.workout.infrastructure.api_data.get_data import APIData


class APIInteractor:
    def __init__(
        self,
        uow: IUnitOfWork,
        api_data: APIData,
        category_map: CategoryToId,
        muscle_map: MuscleGroupToId,
    ) -> None:
        self.UoW = uow
        self.api_data = api_data
        self.category_map = category_map
        self.muscle_map = muscle_map

    async def execute(self) -> None:
        fetched: AsyncIterable[ResponseSchema | None] = self.api_data.fetch_all()
        async for response in fetched:
            if not response:
                break
            result: list[ExerciseSchema] = []
            for item in response.data:
                primary_muscle: str = item.target_muscles[0]
                if not (muscle_g_id := self.muscle_map.get(primary_muscle)):
                    continue
                category: str = item.body_parts[0]
                if not (category_id := self.category_map.get(category)):
                    continue
                schema: ExerciseSchema = ExerciseSchema(
                    name=item.name,
                    description=" ".join(item.description)[:500],
                    exercise_slug=item.exercise_slug,
                    category_id=category_id,
                    muscle_group_id=muscle_g_id,
                )
                result.append(schema)
        if result:
            async with self.UoW:
                logger.info("trying to insert an exercises list")
                await self.UoW.exercise_repository.create_exercises(result)
                await self.UoW.commit()
        logger.info("inserted exercises")

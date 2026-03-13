import sqlalchemy as sa
from dishka import Provider, Scope, provide
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.workout.application.common.dataclasses.categories_dc import (
    CategoryToId,
)
from app.workout.application.common.dataclasses.groups_dc import (
    MuscleGroupToId,
)
from app.workout.infrastructure.db.models.category import Category
from app.workout.infrastructure.db.models.muscle_groups import MuscleGroups


class StaticProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_categories_map(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> CategoryToId:
        async with session_maker() as session:
            logger.info("Entered in context for categories map")
            result = await session.execute(
                sa.select(Category.category, Category.id)
            )
        new_d = {name: index for name, index in result.all()}
        logger.info("Loaded static content: categories map")

        logger.info(f"Loaded keys (Categories) {new_d.keys()}")
        return CategoryToId(new_d)

    @provide
    async def get_muscles_map(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> MuscleGroupToId:
        async with session_maker() as session:
            logger.info("Entered static context for muscle groups map")
            result = await session.execute(
                sa.select(MuscleGroups.groups, MuscleGroups.id)
            )
        new_d = {name: index for name, index in result.all()}
        logger.info("Loaded static content: muscle groups map")
        logger.info(f"Loaded keys(Muscle Groups) {new_d.keys()}")
        return MuscleGroupToId(new_d)

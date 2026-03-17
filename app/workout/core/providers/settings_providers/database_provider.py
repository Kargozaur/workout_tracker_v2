import sys
from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import AsyncAdaptedQueuePool, NullPool

from app.workout.core.settings.db_settings import AbstractDbConfig
from app.workout.core.settings.orm_settings import ORMConfig


class SQLAlchemyProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_engine(
        self, db_cfg: AbstractDbConfig, orm_cfg: ORMConfig
    ) -> AsyncIterable[AsyncEngine]:
        is_celery = "celery" in sys.argv[0]
        """Dishka takes responsibility of SQLAlchemy engine lifetime."""
        params = {}
        if is_celery:
            params["poolclass"] = NullPool
        else:
            params = orm_cfg.model_dump()
            params["poolclass"] = AsyncAdaptedQueuePool
        engine = create_async_engine(
            url=db_cfg.dsn,  # echo=True,
            **params,
        )
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def get_session_maker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            engine,
            expire_on_commit=False,
            autoflush=False,
            class_=AsyncSession,
        )

    @provide(scope=Scope.REQUEST)
    async def create_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

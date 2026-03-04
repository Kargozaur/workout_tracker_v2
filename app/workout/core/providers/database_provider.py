from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.workout.core.settings.db_settings import AbstractDbConfig
from app.workout.core.settings.orm_settings import ORMConfig


class SQLAlchemyProvider(Provider):
    @provide(scope=Scope.APP)
    def get_engine(self, db_cfg: AbstractDbConfig, orm_cfg: ORMConfig) -> AsyncEngine:
        return create_async_engine(url=db_cfg.dsn, **orm_cfg.model_dump())

    @provide(scope=Scope.APP)
    def get_session(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

    @provide(scope=Scope.REQUEST)
    async def create_session(
        self, session_makes: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_makes() as session:
            yield session

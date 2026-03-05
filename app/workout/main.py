from contextlib import asynccontextmanager

from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.workout.core.providers.database_provider import SQLAlchemyProvider
from app.workout.core.providers.security_providers import SecurityProvider
from app.workout.core.providers.settings_provider import ConfigProvider
from app.workout.core.providers.uow_provider import UnitOfWorkProvider
from app.workout.core.providers.use_case_provider import UseCaseProvider
from app.workout.presentation.api.api_router import create_api_router
from app.workout.presentation.api.handlers import (
    create_entity_exception_handler,
    create_user_exception_handler,
)


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    container: AsyncContainer = make_async_container(
        SQLAlchemyProvider(),
        ConfigProvider(),
        SecurityProvider(),
        UnitOfWorkProvider(),
        UseCaseProvider(),
    )

    app.state.container = container
    create_user_exception_handler(app)
    create_entity_exception_handler(app)
    app.include_router(create_api_router())
    setup_dishka(container, app)

    @app.get("/", include_in_schema=False)
    async def start() -> dict:
        return {"start": "Workout app"}

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.container.close()

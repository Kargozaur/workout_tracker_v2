from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.workout.core.providers.database_provider import SQLAlchemyProvider
from app.workout.core.providers.security_providers import SecurityProvider
from app.workout.core.providers.settings_provider import ConfigProvider
from app.workout.core.providers.uow_provider import UnitOfWorkProvider
from app.workout.core.providers.use_case_provider import UseCaseProvider


def create_app() -> FastAPI:
    app = FastAPI()
    container: AsyncContainer = make_async_container(
        SQLAlchemyProvider(),
        ConfigProvider(),
        SecurityProvider(),
        UnitOfWorkProvider(),
        UseCaseProvider(),
    )
    setup_dishka(container, app)
    return app

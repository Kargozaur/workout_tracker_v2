from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.workout.core.providers.database_provider import SQLAlchemyProvider
from app.workout.core.providers.security_providers import SecurityProvider
from app.workout.core.providers.settings_provider import ConfigProvider


def create_app() -> FastAPI:
    app = FastAPI()
    container: AsyncContainer = make_async_container(
        SQLAlchemyProvider(),
        ConfigProvider(),
        SecurityProvider(),
    )
    setup_dishka(container, app)
    return app

from contextlib import asynccontextmanager

from dishka import AsyncContainer, make_async_container
from fastapi import FastAPI

from app.workout.core.providers.database_provider import SQLAlchemyProvider
from app.workout.core.providers.settings_provider import ConfigProvider


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    container: AsyncContainer = make_async_container(
        SQLAlchemyProvider(), ConfigProvider()
    )
    app.state.container = container
    return app


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield
    await app.state.container.stop()
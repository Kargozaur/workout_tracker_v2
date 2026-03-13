from contextlib import asynccontextmanager

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.workout.application.common.dataclasses.categories_dc import (
    CategoryToId,
)
from app.workout.application.common.dataclasses.groups_dc import (
    MuscleGroupToId,
)
from app.workout.core.containers import create_async_containers
from app.workout.core.settings.log_settings import setup_logger
from app.workout.presentation.api.api_router import create_api_router
from app.workout.presentation.exception_handlers import (
    create_auth_exception_handler,
    create_entity_exception_handler,
    create_user_exception_handler,
)
from app.workout.presentation.exception_handlers.workout_handlers import (
    create_workout_exceptions_handler,
)
from app.workout.presentation.middleware.request_time import (
    ProcessTimeMiddleware,
)


def create_app() -> FastAPI:
    setup_logger(default_level="DEBUG")
    app = FastAPI(lifespan=lifespan)
    container: AsyncContainer = create_async_containers()

    app.state.container = container
    app.add_middleware(ProcessTimeMiddleware)
    create_user_exception_handler(app)
    create_entity_exception_handler(app)
    create_auth_exception_handler(app)
    create_workout_exceptions_handler(app)
    app.include_router(create_api_router())
    setup_dishka(container, app)

    @app.get("/", include_in_schema=False)
    async def start() -> dict:
        return {"start": "Workout app"}

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    await app.state.container.get(MuscleGroupToId)
    await app.state.container.get(CategoryToId)
    yield
    await app.state.container.close()

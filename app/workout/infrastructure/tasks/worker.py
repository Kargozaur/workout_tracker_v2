import asyncio

from celery.signals import worker_ready
from dishka.integrations.celery import DishkaTask, FromDishka

from app.workout.application.tasks.commands.api_db_interactor import APIInteractor
from app.workout.application.tasks.commands.cleanup_interactor import (
    CleanupInteractor,
)

from .celery_client import client  # containers


# @client.task(ignore_result=True)
# async def clean_db(interactor: FromDishka[CleanupInteractor]) -> None:
#     await interactor.execute()


# @client.task(ignore_result=True)
# async def get_data(interactor: FromDishka[APIInteractor]) -> None:
#     await interactor.execute()


@client.task(ignore_result=True)
def clean_db() -> None:
    from .celery_client import containers

    async def _run() -> None:
        async with containers() as request_containers:
            interactor = await request_containers.get(CleanupInteractor)
            await interactor.execute()

    asyncio.run(_run())


@client.task(ignore_result=True)
def get_data() -> None:
    from .celery_client import containers

    async def _run() -> None:
        async with containers() as request_containers:
            interactor = await request_containers.get(APIInteractor)
            await interactor.execute()

    asyncio.run(_run())


@worker_ready.connect
def worker_ready(*args, **kwargs) -> None:  # noqa: ANN002, ANN003, ARG001
    """Clean up expired refresh tokens on startup."""
    clean_db.delay()
    get_data.delay()

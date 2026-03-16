import asyncio

from celery.signals import worker_ready
from dishka.integrations.celery import DishkaTask, FromDishka

from app.workout.application.tasks.commands.cleanup_interactor import (
    CleanupInteractor,
)

from .celery_client import client, containers


async def run_clean_db() -> None:
    async with containers() as request_container:
        interactor = await request_container.get(CleanupInteractor)
        await interactor.execute()


@client.task(ignore_result=True)
def clean_db() -> None:
    asyncio.run(run_clean_db())


@worker_ready.connect
def worker_ready() -> None:
    """Clean up expired refresh tokens on startup."""
    clean_db.delay()

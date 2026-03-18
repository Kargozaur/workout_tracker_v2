import asyncio
from typing import cast

from celery import Celery
from celery.schedules import crontab
from celery.signals import worker_shutdown
from dishka import AsyncContainer, Container
from dishka.integrations.celery import DishkaTask, setup_dishka

from app.workout.core.containers import create_async_containers
from app.workout.core.settings.redis_settings import RedisConfig


redis_cfg = RedisConfig()  # type: ignore


def create_celery_client() -> tuple[Celery, AsyncContainer]:
    client = Celery(
        "workout",
        task_cls=DishkaTask,
        broker=f"{redis_cfg.dsn}11",
        backend=f"{redis_cfg.dsn}10",
        include=["app.workout.infrastructure.tasks.worker"],
    )

    client.conf.update(
        task_ignore_result=True,
        broker_connection_retry_on_startup=True,
        timezone="UTC",
    )
    client.conf.beat_schedule = {
        "clean_db": {
            "task": "app.workout.infrastructure.tasks.worker.clean_db",
            "schedule": crontab(minute=0),
        },
        "get_data": {
            "task": "app.workout.infrastructure.tasks.worker.get_data",
            "schedule": crontab(hour=16),
        },
    }

    containers = create_async_containers()
    setup_dishka(cast(Container, containers), client)
    return client, containers


client, containers = create_celery_client()


@worker_shutdown.connect
def shutdown_container(*args, **kwargs) -> None:  # noqa: ANN002, ANN003, ARG001
    try:
        asyncio.run(containers.close())
    except Exception:
        pass

import asyncio
from collections.abc import Mapping, Sequence
from typing import cast

from celery import Celery
from celery.schedules import crontab
from celery.signals import worker_shutdown
from dishka import Container
from dishka.integrations.celery import DishkaTask, setup_dishka

from app.workout.core.containers import create_async_containers
from app.workout.core.settings.redis_settings import RedisConfig


redis_cfg = RedisConfig()

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
    }
}

containers = create_async_containers()

setup_dishka(cast(Container, containers), client)


@worker_shutdown.connect
def shutdown_container() -> None:
    try:
        asyncio.run(containers.close())
    except Exception:
        pass

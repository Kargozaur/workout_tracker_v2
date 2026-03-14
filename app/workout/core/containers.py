from dishka import (
    AsyncContainer,
    make_async_container,
)
from dishka.integrations.fastapi import FastapiProvider

from app.workout.core.providers.app_providers.auth_provider import AuthProvider
from app.workout.core.providers.app_providers.redis_provider import (
    RedisProvider,
)
from app.workout.core.providers.app_providers.service_provider import (
    ServiceProvider,
)
from app.workout.core.providers.app_providers.static_providers import (
    StaticProvider,
)
from app.workout.core.providers.app_providers.uow_provider import (
    UnitOfWorkProvider,
)
from app.workout.core.providers.app_providers.use_case_provider import (
    UseCaseProvider,
)
from app.workout.core.providers.app_providers.workout_provider import (
    WorkoutProvider,
)
from app.workout.core.providers.celery_providers.cleanup_provider import (
    CleanupProvider,
)
from app.workout.core.providers.settings_providers.database_provider import (
    SQLAlchemyProvider,
)
from app.workout.core.providers.settings_providers.httpx_config import (
    HttpxProvider,
)
from app.workout.core.providers.settings_providers.security_providers import (
    SecurityProvider,
)
from app.workout.core.providers.settings_providers.settings_provider import (
    ConfigProvider,
)


def create_async_containers() -> AsyncContainer:
    return make_async_container(
        SQLAlchemyProvider(),
        ConfigProvider(),
        SecurityProvider(),
        UnitOfWorkProvider(),
        UseCaseProvider(),
        AuthProvider(),
        FastapiProvider(),
        RedisProvider(),
        ServiceProvider(),
        CleanupProvider(),
        WorkoutProvider(),
        StaticProvider(),
        HttpxProvider(),
    )

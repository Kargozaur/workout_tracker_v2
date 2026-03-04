from dishka import Provider, Scope, provide

from app.workout.core.settings.db_settings import AbstactDbConfig
from app.workout.core.settings.orm_settings import ORMConfig
from app.workout.core.settings.redis_settings import RedisConfig
from app.workout.core.settings.settings import AppConfig


class ConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_config(self) -> AppConfig:
        return AppConfig()

    @provide
    def get_db_config(self, config: AppConfig) -> AbstactDbConfig:
        return config.db

    @provide
    def get_orm_settings(self, config: AppConfig) -> ORMConfig:
        return config.orm

    @provide
    def get_redis_config(self, config: AppConfig) -> RedisConfig:
        return config.redis

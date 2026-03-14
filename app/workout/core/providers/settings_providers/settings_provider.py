from dishka import Provider, Scope, provide

from app.workout.core.settings.api_settings import APISettings
from app.workout.core.settings.db_settings import AbstractDbConfig
from app.workout.core.settings.jwt_settings import JWTSettings
from app.workout.core.settings.orm_settings import ORMConfig
from app.workout.core.settings.redis_settings import RedisConfig
from app.workout.core.settings.settings import AppConfig


class ConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_config(self) -> AppConfig:
        return AppConfig()

    @provide
    def get_db_config(self, config: AppConfig) -> AbstractDbConfig:
        return config.db

    @provide
    def get_orm_config(self, config: AppConfig) -> ORMConfig:
        return config.orm

    @provide
    def get_redis_config(self, config: AppConfig) -> RedisConfig:
        return config.redis

    @provide
    def get_jwt_config(self, config: AppConfig) -> JWTSettings:
        return config.jwt

    @provide
    def get_api_key(self, config: AppConfig) -> APISettings:
        return config.api
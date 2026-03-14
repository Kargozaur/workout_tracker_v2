from app.workout.core.settings.db_settings import (
    AbstractDbConfig,
    config_factory,
)
from app.workout.core.settings.jwt_settings import JWTSettings
from app.workout.core.settings.orm_settings import ORMConfig, orm_factory
from app.workout.core.settings.redis_settings import RedisConfig
from app.workout.core.settings.api_settings import ApiSettings
from . import BaseSettings, Field, SettingsConfigDict


class AppConfig(BaseSettings):
    db: AbstractDbConfig = Field(default_factory=config_factory)
    orm: ORMConfig = Field(default_factory=orm_factory)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    jwt: JWTSettings = Field(default_factory=JWTSettings)
    api: ApiSettings = Field(default_factory=ApiSettings)

    model_config = SettingsConfigDict(
        arbitrary_types_allowed=True, case_sensitive=False
    )

from typing import Annotated

from pydantic import SecretStr

from . import BaseSettings, Field, RedisDsn, SettingsConfigDict


HOST = Annotated[str, Field(default="localhost")]
PORT = Annotated[int, Field(default=6379)]
DATABASE = Annotated[int, Field(default=0, ge=0, le=16)]
CONNECTIONS = Annotated[int, Field(default=10, gt=0, le=200)]
TIMEOUT = Annotated[float, Field(default=5, gt=0)]


class RedisConfig(BaseSettings):
    host: HOST
    port: PORT
    password: SecretStr
    database: DATABASE
    max_connections: CONNECTIONS
    socket_timeout: TIMEOUT
    connect_timeout: TIMEOUT
    retry_on_timeout: bool = True

    model_config = SettingsConfigDict(
        env_file=".redis.env", env_prefix="REDIS_", extra="ignore"
    )

    @property
    def dsn(self) -> str:
        return str(
            RedisDsn.build(
                scheme="redis",
                host=self.host,
                port=self.port,
                password=self.password.get_secret_value(),
                path=f"/{self.database}",
            )
        )

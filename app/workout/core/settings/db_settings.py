from typing_extensions import Doc

from . import Annotated, BaseSettings, Field, PostgresDsn, SecretStr, SettingsConfigDict


PORT = Annotated[int, Field(default=5432, ge=1, le=65535)]
DRIVER = Annotated[
    str,
    Field(
        default="asyncpg",
    ),
    Doc("Default driver is asyncpg due to asynchronous app"),
]
HOST = Annotated[SecretStr, Field(default="localhost")]


class AbstactDbConfig(BaseSettings):
    model_confgig = SettingsConfigDict(
        env_prefix="DB_", env_file=".db.env", extra="ignore"
    )

    @property
    def dsn(self) -> str:
        raise NotImplementedError()


class PostgresConfig(AbstactDbConfig):
    user: SecretStr
    password: SecretStr
    host: HOST
    database: str
    port: PORT
    driver: DRIVER

    @property
    def dsn(self) -> str:
        return str(
            PostgresDsn.build(
                scheme=f"postgresql+{self.driver}",
                username=self.user.get_secret_value(),
                password=self.password.get_secret_value(),
                host=self.host.get_secret_value() if self.host else "localhost",
                port=self.port,
                path=self.database,
            )
        )


class SQLiteConfig(AbstactDbConfig):
    database: str
    driver: Annotated[str, Field(default="aiosqlite")]

    @property
    def dsn(self) -> str:
        return f"sqlite+{self.driver}:///{self.database}"


def config_factory() -> AbstactDbConfig:
    import os

    from dotenv import load_dotenv

    load_dotenv(".db.env")
    db_type: str = os.getenv("DB_TYPE", "sqlite")
    configs: dict[str, type[AbstactDbConfig]] = {
        "sqlite": SQLiteConfig,
        "postgres": PostgresConfig,
    }
    if db_type.strip().lower() not in configs:
        raise ValueError(f"Unknown database type: {db_type}")

    return configs[db_type]()

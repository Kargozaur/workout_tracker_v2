from . import Annotated, BaseSettings, Field, SettingsConfigDict

POOL_SIZE = Annotated[int, Field(default=10, gt=0)]
OVERFLOW = Annotated[int, Field(default=20, gt=0)]


class ORMConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ORM_", env_file=".orm.env", extra="ignore"
    )


class SQLAlchemy(ORMConfig):
    pool_size: POOL_SIZE
    max_overflow: OVERFLOW


def orm_factory() -> ORMConfig:
    import os

    from dotenv import load_dotenv

    load_dotenv(".orm.env")
    configs: dict[str, type[ORMConfig]] = {"sqlalchemy": SQLAlchemy}
    orm_type = os.getenv("ORM_TYPE", "sqlalchemy")
    if orm_type.strip().lower() not in configs:
        raise ValueError(f"Unknown ORM type: {orm_type}")

    return configs[orm_type]()

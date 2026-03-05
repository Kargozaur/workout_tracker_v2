import datetime as dt
from typing import Any

from pydantic import BeforeValidator, field_validator

from . import Annotated, BaseSettings, Field, SecretStr, SettingsConfigDict


def str_to_timedelta(v: Any) -> Any:
    if isinstance(v, (str, int, float)):
        try:
            return dt.timedelta(seconds=float(v))
        except ValueError:
            return v
    return v


SHORT_EXPIRE = Annotated[
    dt.timedelta,
    BeforeValidator(str_to_timedelta),
    Field(default=dt.timedelta(minutes=30), gt=dt.timedelta(0)),
]
LONG_EXPIRE = Annotated[
    dt.timedelta,
    BeforeValidator(str_to_timedelta),
    Field(default=dt.timedelta(days=7), gt=dt.timedelta(0)),
]


class JWTSettings(BaseSettings):
    token: SecretStr
    expire: SHORT_EXPIRE
    alg: str
    refresh_expire: LONG_EXPIRE

    model_config = SettingsConfigDict(
        env_file=".jwt.env", env_prefix="JWT_", extra="ignore"
    )

    @field_validator("expire", "refresh_expire", mode="before")
    @classmethod
    def parse_seconds(cls, v: Any) -> Any:
        if isinstance(v, str) and v.isdigit():
            return int(v)
        return v

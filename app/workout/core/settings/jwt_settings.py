import datetime as dt

from . import Annotated, BaseSettings, Field, SecretStr, SettingsConfigDict

SHORT_EXPIRE = Annotated[
    dt.timedelta, Field(default=dt.timedelta(minutes=30), gt=0)
]
LONG_EXPIRE = Annotated[
    dt.timedelta, Field(default=dt.timedelta(days=7, gt=0))
]


class JWTSettings(BaseSettings):
    token: SecretStr
    expire: SHORT_EXPIRE
    alg: str
    refresh: LONG_EXPIRE

    model_config = SettingsConfigDict(env_file=".jwt.env", env_prefix="JWT_")

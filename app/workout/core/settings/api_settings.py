from . import BaseSettings, SecretStr, SettingsConfigDict


class APISettings(BaseSettings):
    key: SecretStr

    model_config = SettingsConfigDict(
        env_file=".api.env", extra="ignore", env_prefix="API_"
    )

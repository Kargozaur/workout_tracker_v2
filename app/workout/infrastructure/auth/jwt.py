import datetime as dt
from typing import Any
from uuid import UUID

import jwt

from app.workout.core.settings.jwt_settings import JWTSettings
from app.workout.domains.protocols.itoken import ITokenProvider


class TokenProvider(ITokenProvider):
    def __init__(self, jwt_config: JWTSettings) -> None:
        self.jwt_config = jwt_config

    def _encode(self, user_id: UUID, expire: dt.timedelta) -> str:
        u_id: str = str(user_id)
        to_encode: dict[str, Any] = {"sub": u_id}
        exp: dt.datetime = dt.datetime.utcnow() + expire
        to_encode.update({"exp": exp})
        encoded: str = jwt.encode(
            payload=to_encode,
            key=self.jwt_config.token.get_secret_value(),
            algorithm=self.jwt_config.alg,
        )
        return encoded

    def create_access_token(self, user_id: UUID) -> str:
        encoded: str = self._encode(
            user_id=user_id, expire=self.jwt_config.expire
        )
        return encoded

    def create_refresh_token(self, user_id: UUID) -> str:
        encoded: str = self._encode(
            user_id=user_id, expire=self.jwt_config.refresh_expire
        )
        return encoded

    def decode_token(self, token: str) -> dict[str, Any]:
        try:
            payload: dict[str, Any] = jwt.decode(
                jwt=token,
                key=self.jwt_config.token.get_secret_value(),
                algorithms=[self.jwt_config.alg],
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError()

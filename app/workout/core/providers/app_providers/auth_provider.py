from dishka import Provider, Scope, provide
from fastapi import Request

from app.workout.application.common.types.token_types import (
    AccessToken,
    RefreshToken,
)
from app.workout.domains.exceptions.auth_exceptions import AuthError


class AuthProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_access_token(self, request: Request) -> AccessToken:
        auth_header: str | None = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return AccessToken(auth_header[len("Bearer ") :])
        auth_token: str | None = request.cookies.get("access_token")
        if not auth_token:
            raise AuthError("Unauthorized access")
        return AccessToken(auth_token)

    @provide
    def get_refresh_token(self, request: Request) -> RefreshToken:
        auth_token: str | None = request.cookies.get("refresh_token")
        if not auth_token:
            raise AuthError("Unauthorized access")
        return RefreshToken(auth_token)

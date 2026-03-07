from argon2 import PasswordHasher
from dishka import Provider, Scope, provide

from app.workout.core.settings.settings import AppConfig, JWTSettings
from app.workout.domains.protocols.ihasher import IPasswordHasher
from app.workout.domains.protocols.itoken import ITokenProvider
from app.workout.domains.protocols.itokenhasher import ITokenHasher
from app.workout.infrastructure.auth.hasher import Hasher
from app.workout.infrastructure.auth.jwt import TokenProvider
from app.workout.infrastructure.auth.token_hasher import TokenHasher


class SecurityProvider(Provider):
    scope = Scope.APP

    @provide
    def jwt_settings(self, config: AppConfig) -> JWTSettings:
        return config.jwt

    @provide
    def argon2_hasher(self) -> PasswordHasher:
        return PasswordHasher()

    @provide
    def hasher(self, hasher: PasswordHasher) -> IPasswordHasher:
        return Hasher(hasher)

    @provide
    def token_provider(self, jwt_settings: JWTSettings) -> ITokenProvider:
        return TokenProvider(jwt_settings)

    @provide
    def token_hasher(self) -> ITokenHasher:
        return TokenHasher()

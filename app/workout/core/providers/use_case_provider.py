from dishka import Provider, Scope, decorate, provide
from pydantic import BaseModel

from app.workout.application.auth.get_current_user_cached import (
    CachedUserInteractor,
)
from app.workout.application.auth.get_current_user_interactor import (
    GetUserInteractor,
)
from app.workout.application.auth.login_interactor import LoginInteractor
from app.workout.application.auth.logout_global_interactor import (
    LogoutGlobalInteractor,
)
from app.workout.application.auth.logout_interactor import LogoutInteractor
from app.workout.application.auth.refresh_token_interactor import (
    RefreshTokenInteractor,
)
from app.workout.application.auth.registry_interactor import RegisterUser
from app.workout.application.common.generic_protocols.user_types import (
    CacheUser,
)
from app.workout.application.common.types.token_types import (
    AccessToken,
    RefreshToken,
)
from app.workout.domains.protocols.icacheservice import ICacheService
from app.workout.domains.protocols.ihasher import IPasswordHasher
from app.workout.domains.protocols.itoken import ITokenProvider
from app.workout.domains.protocols.itokenhasher import ITokenHasher
from app.workout.domains.protocols.iuow import IUnitOfWork


class UseCaseProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def register_user_provider(
            self, uow: IUnitOfWork, hasher: IPasswordHasher
    ) -> RegisterUser:
        return RegisterUser(uow, hasher)

    @provide
    def login_provider(
            self,
            uow: IUnitOfWork,
            token_provider: ITokenProvider,
            token_hasher: ITokenHasher,
            password_hasher: IPasswordHasher,
    ) -> LoginInteractor:
        return LoginInteractor(
            uow, token_provider, token_hasher, password_hasher
        )

    @provide
    def current_user_provider(
            self,
            uow: IUnitOfWork,
            access_token: AccessToken,
            token_provider: ITokenProvider,
    ) -> GetUserInteractor:
        return GetUserInteractor(uow, access_token, token_provider)

    @provide
    def logout_provider(
            self,
            uow: IUnitOfWork,
            token_hasher: ITokenHasher,
            refresh_token: RefreshToken,
    ) -> LogoutInteractor:
        return LogoutInteractor(uow, token_hasher, refresh_token)

    @provide
    def logout_global_provider(
            self,
            uow: IUnitOfWork,
            token_provider: ITokenProvider,
            access_token: AccessToken,
    ) -> LogoutGlobalInteractor:
        return LogoutGlobalInteractor(uow, token_provider, access_token)

    @provide
    def refresh_token_provider(
            self,
            uow: IUnitOfWork,
            token_provider: ITokenProvider,
            token_hasher: ITokenHasher,
            refresh_token: RefreshToken,
    ) -> RefreshTokenInteractor:
        return RefreshTokenInteractor(
            uow, token_provider, token_hasher, refresh_token
        )

    @decorate(scope=Scope.REQUEST)
    def cached_interactor(
            self,
            interactor: GetUserInteractor,
            token_provider: ITokenProvider,
            service: ICacheService,
            access_token: AccessToken,
            uow: IUnitOfWork,
    ) -> GetUserInteractor:
        return CachedUserInteractor(
            interactor, token_provider, service, access_token, uow
        )

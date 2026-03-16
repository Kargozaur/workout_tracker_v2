from dishka import Provider, Scope, decorate, provide

from app.workout.application.auth.commands.login_interactor import (
    LoginInteractor,
)
from app.workout.application.auth.commands.logout_global_interactor import (
    LogoutGlobalInteractor,
)
from app.workout.application.auth.commands.logout_interactor import (
    LogoutInteractor,
)
from app.workout.application.auth.commands.refresh_token_interactor import (
    RefreshTokenInteractor,
)
from app.workout.application.auth.commands.registry_interactor import (
    RegisterUser,
)
from app.workout.application.auth.commands.update_profile_interactor import (
    UpdateProfileInteractor,
)
from app.workout.application.auth.queries.get_current_user_cached import (
    CachedUserInteractor,
)
from app.workout.application.auth.queries.get_current_user_interactor import (
    GetUserInteractor,
)
from app.workout.application.common.types.token_types import (
    AccessToken,
    RefreshToken,
)
from app.workout.domains.entities.user_schemas import GetUser, UpdateUser
from app.workout.domains.protocols.auth_protocols.ihasher import (
    IPasswordHasher,
)
from app.workout.domains.protocols.auth_protocols.itoken import ITokenProvider
from app.workout.domains.protocols.auth_protocols.itokenhasher import (
    ITokenHasher,
)
from app.workout.domains.protocols.service_protocols.icacheservice import (
    ICacheService,
)
from app.workout.domains.protocols.uow_protocol.iuow import IUnitOfWork


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
        return LoginInteractor(uow, token_provider, token_hasher, password_hasher)

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
        cache_service: ICacheService[GetUser],
        token_provider: ITokenProvider,
    ) -> LogoutInteractor:
        return LogoutInteractor(
            uow, token_hasher, refresh_token, token_provider, cache_service
        )

    @provide
    def logout_global_provider(
        self,
        uow: IUnitOfWork,
        token_provider: ITokenProvider,
        access_token: AccessToken,
        cache_service: ICacheService[GetUser],
    ) -> LogoutGlobalInteractor:
        return LogoutGlobalInteractor(uow, token_provider, access_token, cache_service)

    @provide
    def refresh_token_provider(
        self,
        uow: IUnitOfWork,
        token_provider: ITokenProvider,
        token_hasher: ITokenHasher,
        refresh_token: RefreshToken,
    ) -> RefreshTokenInteractor:
        return RefreshTokenInteractor(uow, token_provider, token_hasher, refresh_token)

    @decorate
    def cached_interactor(
        self,
        interactor: GetUserInteractor,
        token_provider: ITokenProvider,
        service: ICacheService[GetUser],
        access_token: AccessToken,
        uow: IUnitOfWork,
    ) -> GetUserInteractor:
        """Changes GetUserInteractor with a cached version."""
        return CachedUserInteractor(
            interactor, token_provider, service, access_token, uow
        )

    @provide
    def update_interactor(
        self,
        uow: IUnitOfWork,
        token_provider: ITokenProvider,
        service: ICacheService[UpdateUser],
        access_token: AccessToken,
    ) -> UpdateProfileInteractor:
        return UpdateProfileInteractor(uow, token_provider, service, access_token)

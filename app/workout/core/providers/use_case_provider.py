from dishka import Provider, Scope, provide

from app.workout.application.auth.get_current_user_interactor import (
    GetUserInteractor,
)
from app.workout.application.auth.login_interactor import LoginInteractor
from app.workout.application.auth.registry_interactor import RegisterUser
from app.workout.application.common.types.token_types import AccessToken
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

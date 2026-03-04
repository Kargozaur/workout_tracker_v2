from dishka import Provider, Scope, provide

from app.workout.application.auth.user_interactor import RegisterUser
from app.workout.domains.protocols.ihasher import IPasswordHasher
from app.workout.domains.protocols.iuow import IUnitOfWork


class UseCaseProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def register_user_provider(
            self, uow: IUnitOfWork, hasher: IPasswordHasher
    ) -> RegisterUser:
        return RegisterUser(uow, hasher)

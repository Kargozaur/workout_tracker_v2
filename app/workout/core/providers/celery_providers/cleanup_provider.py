from dishka import Provider, Scope, provide

from app.workout.application.tasks.commands.cleanup_interactor import (
    CleanupInteractor,
)
from app.workout.domains.protocols.uow_protocol.iuow import IUnitOfWork


class CleanupProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def cleanup_interactor(self, uow: IUnitOfWork) -> CleanupInteractor:
        return CleanupInteractor(uow)

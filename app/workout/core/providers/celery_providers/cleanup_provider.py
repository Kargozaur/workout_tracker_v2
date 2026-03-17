from dishka import Provider, Scope, provide

from app.workout.application.common.dataclasses.categories_dc import CategoryToId
from app.workout.application.common.dataclasses.groups_dc import MuscleGroupToId
from app.workout.application.tasks.commands.api_db_interactor import APIInteractor
from app.workout.application.tasks.commands.cleanup_interactor import (
    CleanupInteractor,
)
from app.workout.domains.protocols.uow_protocol.iuow import IUnitOfWork
from app.workout.infrastructure.api_data.get_data import APIData


class CleanupProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def cleanup_interactor(self, uow: IUnitOfWork) -> CleanupInteractor:
        return CleanupInteractor(uow)

    @provide
    def api_interactor(
        self,
        uow: IUnitOfWork,
        api: APIData,
        category: CategoryToId,
        muscle: MuscleGroupToId,
    ) -> APIInteractor:
        return APIInteractor(uow, api, category, muscle)

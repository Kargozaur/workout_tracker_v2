from dishka import Provider, Scope, provide

from app.workout.application.common.types.token_types import AccessToken
from app.workout.application.workouts.commands.add_item import AddItemInteractor
from app.workout.domains.protocols.auth_protocols.itoken import ITokenProvider
from app.workout.domains.protocols.uow_protocol.iuow import IUnitOfWork


class ItemsProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def add_item_interactor(
        self,
        uow: IUnitOfWork,
        access_token: AccessToken,
        token_provider: ITokenProvider,
    ) -> AddItemInteractor:
        return AddItemInteractor(uow, access_token, token_provider)

from dishka import Provider, Scope, provide

from app.workout.application.common.types.token_types import AccessToken
from app.workout.application.workouts.commands.schedule_workout import (
    CreateWorkoutInteractor,
)
from app.workout.domains.protocols.auth_protocols.itoken import ITokenProvider
from app.workout.domains.protocols.uow_protocol.iuow import IUnitOfWork


class WorkoutProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_workout_interactor(
        self,
        uow: IUnitOfWork,
        token_provider: ITokenProvider,
        access_token: AccessToken,
    ) -> CreateWorkoutInteractor:
        return CreateWorkoutInteractor(uow, token_provider, access_token)

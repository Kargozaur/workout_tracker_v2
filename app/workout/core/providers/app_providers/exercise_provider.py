from dishka import Provider, Scope, provide

from app.workout.application.common.types.token_types import AccessToken
from app.workout.application.exercises.queries.get_exercises import GetExercises
from app.workout.domains.protocols.auth_protocols.itoken import ITokenProvider
from app.workout.domains.protocols.uow_protocol.iuow import IUnitOfWork


class ExerciseProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_exercises(
        self,
        uow: IUnitOfWork,
        access_token: AccessToken,
        token_provider: ITokenProvider,
    ) -> GetExercises:
        return GetExercises(uow, access_token, token_provider)

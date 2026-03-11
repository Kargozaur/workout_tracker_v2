from dishka import Provider, Scope, decorate, provide

from app.workout.application.common.types.token_types import AccessToken
from app.workout.application.workouts.commands.schedule_workout import (
    CreateWorkoutInteractor,
)
from app.workout.application.workouts.queries.get_all_workouts import (
    GetAllWorkouts,
)
from app.workout.application.workouts.queries.get_single_workout import (
    GetSingleWorkout,
)
from app.workout.application.workouts.queries.get_single_workout_cached import (
    GetCachedWorkout,
)
from app.workout.domains.entities.workout_schema import WorkoutCache
from app.workout.domains.protocols.auth_protocols.itoken import ITokenProvider
from app.workout.domains.protocols.service_protocols.icacheservice import (
    ICacheService,
)
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

    @provide
    def get_all_workouts_interactor(
        self,
        uow: IUnitOfWork,
        token_provider: ITokenProvider,
        access_token: AccessToken,
    ) -> GetAllWorkouts:
        return GetAllWorkouts(uow, token_provider, access_token)

    @provide
    def get_single_workout_interactor(
        self,
        uow: IUnitOfWork,
        token_provider: ITokenProvider,
        access_token: AccessToken,
    ) -> GetSingleWorkout:
        return GetSingleWorkout(uow, token_provider, access_token)

    @decorate
    def get_single_workout_cache(
        self,
        uow: IUnitOfWork,
        token_provider: ITokenProvider,
        access_token: AccessToken,
        interactor: GetSingleWorkout,
        cache_service: ICacheService[WorkoutCache],
    ) -> GetSingleWorkout:
        return GetCachedWorkout(
            uow, token_provider, access_token, interactor, cache_service
        )

from collections.abc import Awaitable, Callable, Coroutine
from functools import wraps
from typing import Any
from uuid import UUID

from loguru import logger

from app.workout.domains.entities.workout_schema import WorkoutCache


def transactional_workout_cached[**P, R](
    func: Callable[..., Coroutine[Any, Any, R]] | Callable[..., Awaitable[R]],
) -> Callable[..., Coroutine[Any, Any, R]]:
    """Decorator to wrap over commands, that are returning
    DB model. Methods, with which the decorator will be used, must have
    the following attributes:\n
    - token_provider;\n
    - Unit of Work(UoW, must be written exactly like this);\n
    - service(in this case cache service); \n
    - access_token(access_token that will be provide by the dishka).\n
    Doesn't work if function returns anything other than
    DB model. Should be used with the interactors, that will be used
    in put methods(Because they will return the full json response
    rather than dictionary with some message).
    Works only with user_id+workout_id key pair
    (at least for now).\n
    TODO: to consider to leave it as it is, modify it to be more generic,
     or to remove it."""

    @wraps(func)
    async def wrapper(self: object, *args: P.args, **kwargs: P.kwargs) -> R:
        workout_id: UUID = kwargs.get("workout_id")
        user_data: dict[str, Any] = self.token_provider.decode_token(self.access_token)
        user_id: str = user_data.get("sub")
        cache_key: str = f"{user_id}:{workout_id}"
        await self.service.delete_cache(cache_key)
        async with self.UoW:
            logger.debug("Entered transactional_workout_cached context")
            result = await func(self, *args, **kwargs)
            await self.UoW.commit()

        cache: WorkoutCache = WorkoutCache(**result.__dict__)
        await self.service.set_cache(cache_key, cache)
        logger.debug("Set new cache after transaction")
        return result

    return wrapper

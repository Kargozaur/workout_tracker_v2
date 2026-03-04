from . import Any, Awaitable, Callable, Coroutine, IUnitOfWork, wraps


def transactional[**P, R](
        func: Callable[..., Coroutine[Any, Any, R]] | Callable[..., Awaitable[R]],
) -> Callable[..., Coroutine[Any, Any, R]]:
    @wraps(func)
    async def wrapper(self, *args: P.args, **kwargs: P.kwargs) -> R:
        uow: IUnitOfWork | None = getattr(self, "UoW", None)
        if not uow:
            raise AttributeError("Unit of work must be provided")
        async with uow:
            try:
                result = await func(self, *args, **kwargs)
                await uow.commit()
                return result
            except Exception as e:
                await uow.rollback()
                raise e

    return wrapper

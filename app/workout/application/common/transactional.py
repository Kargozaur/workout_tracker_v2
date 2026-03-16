from . import Any, Awaitable, Callable, Coroutine, IUnitOfWork, wraps


def transactional[**P, R](
    func: Callable[..., Coroutine[Any, Any, R]] | Callable[..., Awaitable[R]],
) -> Callable[..., Coroutine[Any, Any, R]]:
    """Transactions manager for a UnitOfWork object.
    Commits changes on success, otherwise rollbacks.
    UnitOfWork attribute must be typed as UoW.
    Decorator should be used only with simple methods that do 1 operation.
    For example bulk deletion from the database, regardless of
    the filters."""

    @wraps(func)
    async def wrapper(self, *args: P.args, **kwargs: P.kwargs) -> R:  # noqa: ANN001
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

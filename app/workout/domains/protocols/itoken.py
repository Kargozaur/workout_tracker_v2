from uuid import UUID

from . import Protocol, runtime_checkable


@runtime_checkable
class ITokenProvider(Protocol):
    async def create_access_token(self, user_id: UUID) -> str: ...

    async def create_refresh_token(self, user_id: UUID) -> str: ...

    async def decode_token(self, token: str) -> bool: ...

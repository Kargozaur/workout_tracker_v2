import datetime as dt
from typing import Protocol
from uuid import UUID


class RefreshTokenT(Protocol):
    id: UUID
    created_at: dt.datetime
    token_hash: str

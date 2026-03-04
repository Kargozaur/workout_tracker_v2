from typing import Protocol, runtime_checkable


@runtime_checkable
class IPasswordHasher(Protocol):
    def hash_password(self, password: str) -> str: ...

    def verify(self, password: str, hashed: str) -> bool: ...

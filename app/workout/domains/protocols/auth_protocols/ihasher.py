from . import Protocol, runtime_checkable


@runtime_checkable
class IPasswordHasher(Protocol):
    def hash_password(self, password: str) -> str: ...

    def verify_password(self, password: str, hashed_password: str) -> bool: ...

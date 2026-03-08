import hashlib

from app.workout.domains.protocols.auth_protocols.itokenhasher import (
    ITokenHasher,
)


class TokenHasher(ITokenHasher):
    def hash(self, token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def verify(self, token: str, hashed_token: str) -> bool:
        return (
            hashlib.sha256(token.encode("utf-8")).hexdigest() == hashed_token
        )

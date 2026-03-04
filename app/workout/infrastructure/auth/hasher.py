from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.workout.domains.protocols.ihasher import IPasswordHasher


class Hasher(IPasswordHasher):
    def __init__(self, hasher: PasswordHasher) -> None:
        self.hasher = hasher

    def hash_password(self, password: str) -> str:
        return self.hasher.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        try:
            return self.hasher.verify(
                self.hasher.verify(password, hashed_password)
            )
        except VerifyMismatchError:
            return False

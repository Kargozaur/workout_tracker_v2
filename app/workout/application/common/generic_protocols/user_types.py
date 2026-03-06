from typing import Protocol
from uuid import UUID


id_types = int | UUID


class User(Protocol):
    email: str


class NotExistingUser(User):
    password: str


class ExistingUser(User):
    id: id_types
    password_hash: str

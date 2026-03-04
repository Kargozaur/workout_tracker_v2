from collections.abc import Awaitable, Callable, Coroutine
from functools import wraps
from typing import Any

from app.workout.domains.protocols.iuow import IUnitOfWork

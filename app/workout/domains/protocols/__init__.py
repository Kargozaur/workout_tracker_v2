from abc import abstractmethod
from typing import Protocol, runtime_checkable

from pydantic import BaseModel

from app.workout.domains.protocols.irepository import IRepository

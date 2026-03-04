from . import BaseModel


class GenericId[T](BaseModel):
    id: T

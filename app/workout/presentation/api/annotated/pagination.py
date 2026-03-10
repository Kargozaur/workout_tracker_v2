from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=10)


PaginationAnnotated = Annotated[PaginationParams, Depends()]

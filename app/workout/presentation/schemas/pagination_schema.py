from pydantic import BaseModel


class PaginatedResponse[T: BaseModel](BaseModel):
    items: list[T]
    page: int
    size: int
    has_next: bool

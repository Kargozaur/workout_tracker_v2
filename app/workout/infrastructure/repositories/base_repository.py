from typing import Any

from pydantic import BaseModel
from sqlalchemy.orm import load_only

from app.workout.domains.exceptions.entity_exceptions import (
    EntityCreationException,
    EntityDeletionException,
    EntityNotFoundException,
    EntityUpdateException,
)
from app.workout.domains.protocols.irepository import IRepository

from . import AsyncSession, sa


class BaseRepository[
ModelT,
CreateSchemaT: BaseModel,
UpdateSchemaT: BaseModel,
](IRepository[ModelT, CreateSchemaT, UpdateSchemaT]):
    def __init__(self, session: AsyncSession, model: type[ModelT]) -> None:
        self.session = session
        self.model = model

    async def get_entity(self, **filters) -> ModelT | None:
        """Generic method to get entity based on filters. It is possible to
        provide fields to load via fields parameter."""
        fields = filters.pop("fields", None)
        query = sa.select(self.model).filter_by(**filters)
        if fields is not None and isinstance(fields, (list, tuple)):
            load_fields = [
                getattr(self.model, f)
                for f in fields
                if hasattr(self.model, f)
            ]
            if load_fields:
                query = query.options(load_only(*load_fields))
        print(f"SQL: {query.compile(compile_kwargs={'literal_binds': True})}")
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_entity(self, attributes: CreateSchemaT) -> ModelT | None:
        """Creates entity based on pydantic schema provided."""
        model: ModelT = self.model(**attributes.model_dump(by_alias=True))
        try:
            self.session.add(model)
            await self.session.flush()
            return model
        except Exception as exc:
            raise EntityCreationException() from exc

    async def update_entity(
            self, attributes: UpdateSchemaT, **filters: object
    ) -> ModelT:
        """Updates entity based on pydantic schema provided. Filters are applied
        based on method call."""
        entity: ModelT | None = await self.get_entity(**filters)
        if entity is None:
            raise EntityNotFoundException("Entity not found")
        data: dict[str, Any] = attributes.model_dump(exclude_unset=True)
        try:
            for k, v in data.items():
                if hasattr(entity, k):
                    setattr(entity, k, v)
            await self.session.refresh(entity)
            return entity
        except Exception as exc:
            raise EntityUpdateException() from exc

    async def delete_entity(self, **filters: object) -> bool:
        """Deletes entity from the database based on filters."""
        entity: ModelT | None = await self.get_entity(**filters)
        if entity is None:
            return False
        try:
            await self.session.delete(entity)
            await self.session.flush()
            return True
        except Exception as exc:
            raise EntityDeletionException() from exc

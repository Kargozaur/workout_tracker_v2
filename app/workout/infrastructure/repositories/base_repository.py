import datetime as dt
from typing import Any

from loguru import logger
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
    """Base repository for all repositories that are using SQLAlchemy sessions.
    CRUD functionality provided by methods:
    get_entity
    create_entity
    update_entity
    delete_entity
    """

    def __init__(self, session: AsyncSession, model: type[ModelT]) -> None:
        self.session = session
        self.model = model

    async def get_entity(self, **filters: object) -> ModelT | None:
        """Generic method to get an entity based on filters. It is possible to
        provide fields to load via fields keyword parameter.
        When passed, fields should look like: (...other kwargs, fields=("id", "name", etc.)).
        fields must be passed as tuple."""
        fields = filters.pop("fields", None)
        query = sa.select(self.model).filter_by(**filters)
        if fields is not None and isinstance(fields, tuple):
            load_fields = [
                attr
                for f in fields
                if (attr := getattr(self.model, f, None)) is not None
            ]
            if load_fields:
                query = query.options(load_only(*load_fields))
        logger.debug(
            f"SQL: {query.compile(compile_kwargs={'literal_binds': True})}"
        )
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
            logger.exception("Failed to create entity")
            raise EntityCreationException() from exc

    async def update_entity(
        self, attributes: UpdateSchemaT, **filters: object
    ) -> ModelT:
        """Updates entity based on pydantic schema provided. Filters are applied
        based on given kwargs."""
        entity: ModelT | None = await self.get_entity(**filters)
        if entity is None:
            raise EntityNotFoundException("Entity not found")
        data: dict[str, Any] = attributes.model_dump(
            exclude_unset=True, by_alias=True
        )
        try:
            for k, v in data.items():
                if hasattr(entity, k):
                    setattr(entity, k, v)

            await self.session.flush()
            await self.session.refresh(entity)
            return entity
        except Exception as exc:
            logger.exception("Failed to update entity")
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
            logger.exception("Failed to delete entity")
            raise EntityDeletionException() from exc

    async def delete_expired(self) -> bool:
        """Deletes expired entities from the database."""
        now: dt.datetime = dt.datetime.now(dt.UTC)
        query = sa.delete(self.model).where(self.model.expires_at < now)
        try:
            await self.session.execute(query)
            return True
        except Exception as exc:
            logger.exception("Failed to delete expired entities")
            raise EntityDeletionException() from exc

    async def bulk_deletion(self, **filters: object):
        query = sa.delete(self.model).filter_by(**filters)
        try:
            await self.session.execute(query)
            return True
        except Exception as exc:
            logger.exception("Failed to delete entities")
            raise EntityDeletionException() from exc

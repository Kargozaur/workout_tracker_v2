from . import BaseModel, Protocol, runtime_checkable


@runtime_checkable
class IRepository[
    ModelT,
    CreateSchemaT: BaseModel,
    UpdateSchemaT: BaseModel | None = None,
](Protocol):
    async def get_entity(self, **filters: object) -> ModelT: ...

    async def create_entity(self, schema: CreateSchemaT) -> ModelT: ...

    async def update_entity(
        self, attributes: UpdateSchemaT, **filters: object
    ) -> ModelT: ...

    async def delete_entity(self, **filters: object) -> bool: ...

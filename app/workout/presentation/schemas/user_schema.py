from . import UUID, ConfigDict, Field, GenericId, dt


class GetUser(GenericId[UUID]):
    email: str
    first_name: str = Field(serialization_alias="firstName")
    last_name: str = Field(serialization_alias="lastName")
    created_at: dt.datetime = Field(serialization_alias="createdAt")
    updated_at: dt.datetime = Field(serialization_alias="updatedAt")

    model_config = ConfigDict(from_attributes=True)

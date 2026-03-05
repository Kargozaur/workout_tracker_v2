from . import UUID, ConfigDict, GenericId, dt


class GetUser(GenericId[UUID]):
    email: str
    first_name: str
    last_name: str
    created_at: dt.datetime
    updated_at: dt.datetime

    model_config = ConfigDict(from_attributes=True)

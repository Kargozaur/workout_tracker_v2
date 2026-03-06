from pydantic import BaseModel, Field


class LogoutSchema(BaseModel):
    success: str = Field(
        default="You have been logged out", serialization_alias="Success"
    )

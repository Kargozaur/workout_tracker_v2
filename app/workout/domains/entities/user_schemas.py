import datetime as dt
from typing import Self
from uuid import UUID

from app.workout.application.common.verify_password import verify_password

from . import (
    Annotated,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    EmailStr,
    Field,
    GenericId,
    model_validator,
)


GenericStr = Annotated[str | None, Field(default=None, min_length=1)]
PasswordField = Annotated[str, BeforeValidator(verify_password)]


class CreateUser(BaseModel):
    email: EmailStr
    password: PasswordField = Field(
        validation_alias="password", alias="password_hash"
    )
    first_name: GenericStr
    last_name: GenericStr

    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="after")
    def set_name_if_not_provided(self) -> Self:
        if not self.first_name and self.last_name:
            self.first_name = (
                self.email.split("@")[0][: len(self.email) // 2]
                .replace("_", "")
                .replace(".", "")
            )
            self.last_name: str = (
                self.email.split("@")[0][len(self.email) // 2 :]
                .replace("_", "")
                .replace(".", "")
            )
        if not self.first_name:
            self.first_name: str = (
                self.email.split("@")[0][: len(self.email) // 2]
                .replace("_", "")
                .replace(".", "")
            )
        if not self.last_name:
            self.last_name: str = (
                self.email.split("@")[0][len(self.email) // 2 :]
                .replace("_", "")
                .replace(".", "")
            )

        return self


class UpdateUser(BaseModel):
    email: EmailStr | None = None
    new_password: PasswordField | None = Field(alias="password_hash")
    first_name: GenericStr
    last_name: GenericStr


class LoginSchema(BaseModel):
    email: str
    password: str


class GetUser(GenericId[UUID]):
    email: str
    first_name: str
    last_name: str
    created_at: dt.datetime
    updated_at: dt.datetime

    model_config = ConfigDict(from_attributes=True)

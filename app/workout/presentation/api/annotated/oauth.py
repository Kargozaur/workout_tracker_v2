from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.workout.presentation.api.oauth.custom_oath2password_bearer import OAuth2HeaderOrCookie


oauth2_scheme = OAuth2HeaderOrCookie(
    tokenUrl="/api/v1/auth/login", auto_error=False
)

OAuth2 = Annotated[str | None, Depends(oauth2_scheme)]
Form_data = Annotated[OAuth2PasswordRequestForm, Depends()]

from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login", auto_error=False
)

OAuth2 = Annotated[str | None, Depends(oauth2_scheme)]
Form_data = Annotated[OAuth2PasswordRequestForm, Depends()]

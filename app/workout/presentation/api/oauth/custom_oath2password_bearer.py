from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer


class OAuth2HeaderOrCookie(OAuth2PasswordBearer):
    """Custom OAuth2 class to allow both cookie and header authentication
    for the OAuth2PasswordRequestForm."""

    async def __call__(self, request: Request):  # noqa: ANN204
        header = request.headers.get("Authorization")
        cookie = request.cookies.get("access_token")
        if header and " " in header:
            parts = header.split(" ")
            if parts[0].lower().strip() == "bearer":
                return parts[1]

        if cookie:
            return cookie
        if self.auto_error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )
        return None

from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer


class OAuth2HeaderOrCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request):
        header = request.headers.get("Authorization")
        cookie = request.cookies.get("access_token")
        if header:
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

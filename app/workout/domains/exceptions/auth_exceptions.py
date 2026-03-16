from app.workout.application.common.status_codes import failed_status_codes

from .app_base_exception import AppBaseException


class AuthException(AppBaseException):
    status_code = failed_status_codes.unauthorized

    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(message)


class TokenExpiredException(AppBaseException):
    status_code = failed_status_codes.not_found

    def __init__(self, message: str = "Token Expired") -> None:
        super().__init__(message)

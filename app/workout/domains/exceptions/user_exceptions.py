from app.workout.application.common.status_codes import failed_status_codes

from .app_base_exception import AppBaseException


class UserExistsException(AppBaseException):
    status_code = failed_status_codes.conflict

    def __init__(self, message: str = "User already exists") -> None:
        super().__init__(message)


class UserFailedToCreateException(AppBaseException):
    status_code = failed_status_codes.bad_request

    def __init__(self, message: str = "Failed to create user") -> None:
        super().__init__(message)


class UserNotFoundException(AppBaseException):
    status_code = failed_status_codes.not_found

    def __init__(self, message: str = "User not found") -> None:
        super().__init__(message)


class UserUpdateFail(AppBaseException):
    status_code = failed_status_codes.unprocessable_content

    def __init__(self, message: str = "Failed to update user") -> None:
        super().__init__(message)

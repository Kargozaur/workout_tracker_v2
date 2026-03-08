from app.workout.application.common.status_codes import failed_status_codes

from .app_base_exception import AppBaseException


class EntityCreationException(AppBaseException):
    status_code = failed_status_codes.bad_request

    def __init__(self, message: str = "Entity creation failed") -> None:
        super().__init__(message)


class EntityDeletionException(AppBaseException):
    status_code = failed_status_codes.bad_request

    def __init__(self, message: str = "Entity deletion failed") -> None:
        super().__init__(message)


class EntityUpdateException(AppBaseException):
    status_code = failed_status_codes.bad_request

    def __init__(self, message: str = "Entity update failed") -> None:
        super().__init__(message)


class EntityNotFoundException(AppBaseException):
    status_code = failed_status_codes.not_found

    def __init__(self, message: str = "Entity not found") -> None:
        super().__init__(message)

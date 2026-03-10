from app.workout.application.common.status_codes import failed_status_codes

from .app_base_exception import AppBaseException


class WorkoutStartException(AppBaseException):
    status_code = failed_status_codes.bad_request

    def __init__(self, message: str = "Failed to start workout") -> None:
        super().__init__(message)


class WorkoutEndException(AppBaseException):
    status_code = failed_status_codes.bad_request

    def __init__(self, message: str = "Failed to end workout") -> None:
        super().__init__(message)


class WorkoutNotFoundException(AppBaseException):
    status_code = failed_status_codes.not_found

    def __init__(self, message: str = "Workout not found") -> None:
        super().__init__(message)

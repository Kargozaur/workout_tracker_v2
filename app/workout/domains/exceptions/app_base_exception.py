from app.workout.application.common.status_codes import failed_status_codes


class AppBaseError(Exception):
    status_code = failed_status_codes.server_error

    def __init__(self, message: str = "App base exception") -> None:
        super().__init__()
        self.message = message

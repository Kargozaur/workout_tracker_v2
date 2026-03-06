from app.workout.application.common.status_codes import failed_status_codes


class UserException(Exception):
    status_code = failed_status_codes.server_error
    message = "User exception"


class UserExistsException(UserException):
    status_code = failed_status_codes.conflict
    message = "User already exists"


class UserFailedToCreateException(UserException):
    status_code = failed_status_codes.bad_request
    message = "Failed to create user"


class UserNotFoundException(UserException):
    status_code = failed_status_codes.not_found
    message = "User not found"


class UserUpdateFail(UserException):
    status_code = failed_status_codes.unprocessable_content
    message = "Failed to update user"

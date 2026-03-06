from app.workout.application.common.status_codes import failed_status_codes


class AuthException(Exception):
    status_code = failed_status_codes.unauthorized
    message = "Unauthorized"


class TokenExpiredException(AuthException):
    status_code = failed_status_codes.not_found
    message = "Token expired"

from app.workout.application.common.status_codes import failed_status_codes


class AuthException(Exception):
    status_code = failed_status_codes.unauthorized
    message = "Unauthorized"

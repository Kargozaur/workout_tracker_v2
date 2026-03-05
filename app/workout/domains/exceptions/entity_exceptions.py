from app.workout.application.common.status_codes import bad_status_codes


class EntityBaseException(Exception):
    status_code = bad_status_codes.server_error
    message = "Entity base exception"


class EntityCreationException(EntityBaseException):
    status_code = bad_status_codes.bad_request
    message = "Entity creation failed"


class EntityDeletionException(EntityBaseException):
    status_code = bad_status_codes.bad_request
    message = "Entity deletion failed"


class EntityUpdateException(EntityBaseException):
    status_code = bad_status_codes.bad_request
    message = "Entity update failed"


class EntityNotFoundException(EntityBaseException):
    status_code = bad_status_codes.not_found
    message = "Entity not found"

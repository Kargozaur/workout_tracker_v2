from app.workout.application.common.status_codes import bad_status_codes


class EntityBaseException(Exception):
    status = bad_status_codes.server_error
    message = "Entity base exception"


class EntityCreationException(EntityBaseException):
    status = bad_status_codes.bad_request
    message = "Entity creation failed"


class EntityDeletionException(EntityBaseException):
    status = bad_status_codes.bad_request
    message = "Entity deletion failed"


class EntityUpdateException(EntityBaseException):
    status = bad_status_codes.bad_request
    message = "Entity update failed"


class EntityNotFoundException(EntityBaseException):
    status = bad_status_codes.not_found
    message = "Entity not found"

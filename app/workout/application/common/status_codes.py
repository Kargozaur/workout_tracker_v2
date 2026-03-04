from collections import namedtuple

BadRequests = namedtuple(
    "BadRequests",
    (
        "bad_request",
        "unauthorized",
        "not_found",
        "conflict",
        "unprocessable_content",
        "server_error",
    ),
)

SuccessStatusCodes = namedtuple("Success", ("ok", "success", "no_content"))

bad_status_codes = BadRequests(400, 401, 404, 409, 422, 500)
success_status_codes = SuccessStatusCodes(200, 201, 204)

from typing import Final, NamedTuple


class BadRequests(NamedTuple):
    """Failure status codes."""

    bad_request: int
    unauthorized: int
    not_found: int
    conflict: int
    unprocessable_content: int
    server_error: int


class SuccessStatusCodes(NamedTuple):
    """Success status codes."""

    ok: int
    success: int
    no_content: int


failed_status_codes: Final[BadRequests] = BadRequests(
    bad_request=400,
    unauthorized=401,
    not_found=404,
    conflict=409,
    unprocessable_content=422,
    server_error=500,
)

success_status_codes: Final[SuccessStatusCodes] = SuccessStatusCodes(
    ok=200, success=201, no_content=204
)

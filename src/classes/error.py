class BadRequestError(Exception):
    """Your request has missing arguments or is malformed."""

class UnauthorizedError(Exception):
    """Your request is not authenticated."""

class ForbiddenError(Exception):
    """Your request is authenticated but has insufficient permissions."""

class MethodNotAllowedError(Exception):
    """You are using an incorrect HTTP verb. Double check whether it should be POST/GET/DELETE/etc."""

class PageNotFoundError(Exception):
    """The endpoint requested does not exist."""

class NotAcceptableError(Exception):
    """Your application does not accept the content format returned according to the Accept headers sent in the request."""

class TooManyRequestsError(Exception):
    """Your application is exceeding its rate limit. Back off, buddy. :p"""

class InternalServerError(Exception):
    """Something is wrong on our end. Whoopsie."""

class GatewayTimeoutError(Exception):
    """Something has timed out on our end. Whoopsie."""
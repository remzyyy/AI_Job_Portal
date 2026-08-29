class AppException(Exception):
    """Base exception with status code and message."""

    def __init__(self, status_code: int, detail: str, field: str = None):
        self.status_code = status_code
        self.detail = detail
        self.field = field


class NotFoundError(AppException):
    def __init__(self, resource: str, identifier):
        super().__init__(404, f"{resource} with id {identifier} not found")


class AuthorizationError(AppException):
    def __init__(self):
        super().__init__(403, "You do not have permission to perform this action")


class ValidationError(AppException):
    def __init__(self, detail: str, field: str = None):
        super().__init__(400, detail, field)


class ConflictError(AppException):
    def __init__(self, detail: str):
        super().__init__(409, detail)


class ServiceUnavailableError(AppException):
    def __init__(self, service: str):
        super().__init__(503, f"{service} is temporarily unavailable. Please retry later.")

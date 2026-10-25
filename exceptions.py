"""Domain exceptions.

Services raise these framework-agnostic errors; ``app.main`` maps each one to
an HTTP status code in a single place, keeping services free of HTTP concerns.
"""


class DomainError(Exception):
    """Base class for all expected business-rule failures."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NotFoundError(DomainError):
    """The requested resource does not exist."""


class ConflictError(DomainError):
    """The request conflicts with existing state (e.g. duplicate email)."""


class InsufficientStockError(ConflictError):
    """A purchase asked for more units than are in stock."""


class AuthenticationError(DomainError):
    """Credentials or token are missing or invalid."""


class PermissionDeniedError(DomainError):
    """The user is authenticated but not allowed to perform the action."""


class ValidationError(DomainError):
    """The request is well-formed but violates a business rule."""

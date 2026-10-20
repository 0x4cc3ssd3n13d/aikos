class DomainError(Exception):
    """Base class for rule violations in the domain."""


class InvalidInput(DomainError):
    """Raised when a value breaks a domain rule, such as an empty note."""

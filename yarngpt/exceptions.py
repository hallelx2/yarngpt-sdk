"""Exceptions for YarnGPT SDK."""


class YarnGPTError(Exception):
    """Base exception for all YarnGPT SDK errors."""
    pass


class AuthenticationError(YarnGPTError):
    """Raised when API authentication fails."""
    pass


class ValidationError(YarnGPTError):
    """Raised when request parameters are invalid."""
    pass


class APIError(YarnGPTError):
    """Raised when an API request fails."""
    pass

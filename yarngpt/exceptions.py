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


class QuotaExceededError(APIError):
    """
    Raised when API quota is exceeded or rate limit is reached.

    YarnGPT daily limits (free tier):
    - TTS Requests: 80/day
    - Media Processing Jobs: 8/day
    - URL Extractions: 100/day
    - Chunked Audio Generations: 120/day
    """

    pass


class PaymentRequiredError(APIError):
    """Raised when payment is required to continue using the API."""

    pass

"""YarnGPT SDK - Unofficial community Python SDK for YarnGPT Text-to-Speech API."""

from .client import YarnGPT
from .async_client import AsyncYarnGPT
from .models import Voice, AudioFormat
from .retry import RetryConfig
from .exceptions import (
    YarnGPTError,
    AuthenticationError,
    ValidationError,
    APIError,
    QuotaExceededError,
    PaymentRequiredError,
)

__version__ = "0.1.0"
__all__ = [
    "YarnGPT",
    "AsyncYarnGPT",
    "Voice",
    "AudioFormat",
    "RetryConfig",
    "YarnGPTError",
    "AuthenticationError",
    "ValidationError",
    "APIError",
    "QuotaExceededError",
    "PaymentRequiredError",
]

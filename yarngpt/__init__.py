"""YarnGPT SDK - Unofficial community Python SDK for YarnGPT Text-to-Speech API."""

from .client import YarnGPT
from .models import Voice, AudioFormat
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
    "Voice",
    "AudioFormat",
    "YarnGPTError",
    "AuthenticationError",
    "ValidationError",
    "APIError",
    "QuotaExceededError",
    "PaymentRequiredError",
]

"""YarnGPT SDK - Text-to-Speech API for Nigerian Accents."""

from .client import YarnGPT
from .models import Voice, AudioFormat
from .exceptions import YarnGPTError, AuthenticationError, ValidationError, APIError

__version__ = "0.1.0"
__all__ = [
    "YarnGPT",
    "Voice",
    "AudioFormat",
    "YarnGPTError",
    "AuthenticationError",
    "ValidationError",
    "APIError",
]

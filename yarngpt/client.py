"""YarnGPT API Client."""

from typing import Optional, Union
from pathlib import Path
import httpx

from .models import Voice, AudioFormat
from .exceptions import YarnGPTError, AuthenticationError, ValidationError, APIError


class YarnGPT:
    """
    YarnGPT Text-to-Speech API Client.
    
    This client provides access to YarnGPT's Nigerian accent text-to-speech API.
    
    Args:
        api_key: Your YarnGPT API key. Get it from https://yarngpt.ai/account
        base_url: Base URL for the API (default: https://yarngpt.ai/api/v1)
        timeout: Request timeout in seconds (default: 30)
    
    Example:
        >>> client = YarnGPT(api_key="your_api_key")
        >>> audio = client.text_to_speech("Hello, how are you?", voice=Voice.IDERA)
        >>> with open("output.mp3", "wb") as f:
        ...     f.write(audio)
    """
    
    DEFAULT_BASE_URL = "https://yarngpt.ai/api/v1"
    MAX_TEXT_LENGTH = 2000
    
    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: float = 30.0
    ):
        """Initialize the YarnGPT client."""
        if not api_key:
            raise AuthenticationError("API key is required")
        
        self.api_key = api_key
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.timeout = timeout
        
        self._client = httpx.Client(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    def close(self):
        """Close the HTTP client."""
        self._client.close()
    
    def text_to_speech(
        self,
        text: str,
        voice: Optional[Union[Voice, str]] = None,
        response_format: Optional[Union[AudioFormat, str]] = None,
    ) -> bytes:
        """
        Convert text to speech using YarnGPT's API.
        
        Args:
            text: The text to convert to speech (max 2000 characters)
            voice: Voice character to use (defaults to 'Idera')
            response_format: Audio format: mp3, wav, opus, or flac (defaults to mp3)
        
        Returns:
            bytes: Audio data in the requested format
        
        Raises:
            ValidationError: If text is too long or parameters are invalid
            AuthenticationError: If API key is invalid
            APIError: If the API request fails
        
        Example:
            >>> client = YarnGPT(api_key="your_api_key")
            >>> audio = client.text_to_speech(
            ...     "Welcome to Nigeria!",
            ...     voice=Voice.EMMA,
            ...     response_format=AudioFormat.MP3
            ... )
        """
        # Validate text length
        if not text:
            raise ValidationError("Text cannot be empty")
        
        if len(text) > self.MAX_TEXT_LENGTH:
            raise ValidationError(
                f"Text length ({len(text)}) exceeds maximum of {self.MAX_TEXT_LENGTH} characters"
            )
        
        # Prepare request payload
        payload = {"text": text}
        
        if voice is not None:
            if isinstance(voice, Voice):
                payload["voice"] = voice.value
            else:
                payload["voice"] = str(voice)
        
        if response_format is not None:
            if isinstance(response_format, AudioFormat):
                payload["response_format"] = response_format.value
            else:
                payload["response_format"] = str(response_format)
        
        # Make API request
        try:
            response = self._client.post(
                f"{self.base_url}/tts",
                json=payload,
            )
            
            # Handle response
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key")
            elif response.status_code == 400:
                error_msg = "Invalid request parameters"
                try:
                    error_data = response.json()
                    error_msg = error_data.get("error", error_msg)
                except Exception:
                    pass
                raise ValidationError(error_msg)
            elif response.status_code != 200:
                raise APIError(
                    f"API request failed with status {response.status_code}: {response.text}"
                )
            
            return response.content
            
        except httpx.TimeoutException as e:
            raise APIError(f"Request timed out: {e}")
        except httpx.RequestError as e:
            raise APIError(f"Request failed: {e}")
    
    def text_to_speech_file(
        self,
        text: str,
        output_path: Union[str, Path],
        voice: Optional[Union[Voice, str]] = None,
        response_format: Optional[Union[AudioFormat, str]] = None,
    ) -> Path:
        """
        Convert text to speech and save directly to a file.
        
        Args:
            text: The text to convert to speech (max 2000 characters)
            output_path: Path where the audio file will be saved
            voice: Voice character to use (defaults to 'Idera')
            response_format: Audio format: mp3, wav, opus, or flac (defaults to mp3)
        
        Returns:
            Path: Path to the saved audio file
        
        Example:
            >>> client = YarnGPT(api_key="your_api_key")
            >>> path = client.text_to_speech_file(
            ...     "Hello World!",
            ...     "output.mp3",
            ...     voice=Voice.JUDE
            ... )
        """
        audio_data = self.text_to_speech(
            text=text,
            voice=voice,
            response_format=response_format,
        )
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "wb") as f:
            f.write(audio_data)
        
        return output_path

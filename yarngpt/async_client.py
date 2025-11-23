"""Async client for YarnGPT API."""

from typing import Optional, Union, List, Dict
from pathlib import Path
import httpx
from decouple import config

from .models import Voice, AudioFormat
from .exceptions import (
    AuthenticationError,
    ValidationError,
    APIError,
    QuotaExceededError,
    PaymentRequiredError,
)
from .retry import RetryConfig, with_retry_async


class AsyncYarnGPT:
    """
    Async YarnGPT Text-to-Speech API Client.
    
    This async client provides non-blocking access to YarnGPT's Nigerian accent TTS API.
    Ideal for web applications, high-volume processing, and concurrent operations.
    
    Args:
        api_key: Your YarnGPT API key. Get it from https://yarngpt.ai/account
        base_url: Base URL for the API (default: https://yarngpt.ai/api/v1)
        timeout: Request timeout in seconds (default: 30)
        retry_config: Retry configuration for failed requests
        
    Example:
        >>> async with AsyncYarnGPT(api_key="your_api_key") as client:
        ...     audio = await client.text_to_speech("Hello!", voice=Voice.IDERA)
        ...     with open("output.mp3", "wb") as f:
        ...         f.write(audio)
    """
    
    DEFAULT_BASE_URL = "https://yarngpt.ai/api/v1"
    MAX_TEXT_LENGTH = 2000
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        retry_config: Optional[RetryConfig] = None,
    ):
        """Initialize the async YarnGPT client."""
        # Auto-load API key from environment if not provided
        if api_key is None:
            api_key = config("YARNGPT_API_KEY", default="")
        
        if not api_key:
            raise AuthenticationError(
                "API key is required. Set YARNGPT_API_KEY environment variable or pass api_key parameter."
            )
        
        self.api_key = api_key
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.timeout = timeout
        self.retry_config = retry_config or RetryConfig()
        
        self._client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self._client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=self.timeout,
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    def _ensure_client(self):
        """Ensure client is initialized."""
        if self._client is None:
            raise RuntimeError(
                "Client not initialized. Use 'async with AsyncYarnGPT() as client:' "
                "or call client._client manually."
            )
    
    @with_retry_async()
    async def _make_request(self, payload: dict) -> bytes:
        """Make API request with retry logic."""
        self._ensure_client()
        
        response = await self._client.post(
            f"{self.base_url}/tts",
            json=payload,
        )
        
        # Handle response
        if response.status_code == 401:
            raise AuthenticationError("Invalid API key")
        elif response.status_code == 429:
            error_msg = (
                "Daily API quota exceeded. "
                "YarnGPT free tier limits: 80 TTS requests/day. "
                "Please wait 24 hours or upgrade your account at https://yarngpt.ai/account"
            )
            try:
                error_data = response.json()
                error_msg = error_data.get("error", error_msg)
            except Exception:
                pass
            raise QuotaExceededError(error_msg)
        elif response.status_code == 400:
            error_msg = "Invalid request parameters"
            try:
                error_data = response.json()
                error_msg = error_data.get("error", error_msg)
            except Exception:
                pass
            raise ValidationError(error_msg)
        elif response.status_code == 402:
            raise PaymentRequiredError(
                "Payment required. Please check your account balance or subscription."
            )
        elif response.status_code == 403:
            raise AuthenticationError(
                "Access forbidden. Please check your API key permissions."
            )
        elif response.status_code != 200:
            raise APIError(
                f"API request failed with status {response.status_code}: {response.text}"
            )
        
        return response.content
    
    async def text_to_speech(
        self,
        text: str,
        voice: Optional[Union[Voice, str]] = None,
        response_format: Optional[Union[AudioFormat, str]] = None,
    ) -> bytes:
        """
        Convert text to speech using YarnGPT's API (async).
        
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
            >>> async with AsyncYarnGPT() as client:
            ...     audio = await client.text_to_speech(
            ...         "Welcome to Nigeria!",
            ...         voice=Voice.EMMA,
            ...         response_format=AudioFormat.MP3
            ...     )
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
        
        # Make API request with retry logic
        try:
            return await self._make_request(payload)
        except httpx.TimeoutException as e:
            raise APIError(f"Request timed out: {e}")
        except httpx.RequestError as e:
            raise APIError(f"Request failed: {e}")
    
    async def text_to_speech_file(
        self,
        text: str,
        output_path: Union[str, Path],
        voice: Optional[Union[Voice, str]] = None,
        response_format: Optional[Union[AudioFormat, str]] = None,
    ) -> Path:
        """
        Convert text to speech and save directly to a file (async).
        
        Args:
            text: The text to convert to speech (max 2000 characters)
            output_path: Path where the audio file will be saved
            voice: Voice character to use (defaults to 'Idera')
            response_format: Audio format: mp3, wav, opus, or flac (defaults to mp3)
            
        Returns:
            Path: Path to the saved audio file
        """
        audio_data = await self.text_to_speech(
            text=text,
            voice=voice,
            response_format=response_format,
        )
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "wb") as f:
            f.write(audio_data)
        
        return output_path
    
    async def batch_text_to_speech(
        self,
        texts: List[str],
        voice: Optional[Union[Voice, str]] = None,
        response_format: Optional[Union[AudioFormat, str]] = None,
        concurrent: bool = True,
    ) -> List[bytes]:
        """
        Convert multiple texts to speech in batch (async with optional concurrency).
        
        Args:
            texts: List of texts to convert to speech (each max 2000 characters)
            voice: Voice character to use for all texts (defaults to 'Idera')
            response_format: Audio format for all outputs (defaults to mp3)
            concurrent: If True, process requests concurrently (default: True)
            
        Returns:
            List[bytes]: List of audio data in the requested format
            
        Example:
            >>> async with AsyncYarnGPT() as client:
            ...     texts = ["Hello", "Welcome", "Goodbye"]
            ...     audios = await client.batch_text_to_speech(texts, concurrent=True)
        """
        import asyncio
        
        if concurrent:
            # Process all texts concurrently
            tasks = [
                self.text_to_speech(text=text, voice=voice, response_format=response_format)
                for text in texts
            ]
            return await asyncio.gather(*tasks)
        else:
            # Process sequentially
            results = []
            for text in texts:
                audio = await self.text_to_speech(
                    text=text,
                    voice=voice,
                    response_format=response_format,
                )
                results.append(audio)
            return results
    
    async def batch_text_to_speech_files(
        self,
        texts: List[str],
        output_dir: Union[str, Path],
        filename_prefix: str = "audio",
        voice: Optional[Union[Voice, str]] = None,
        response_format: Optional[Union[AudioFormat, str]] = None,
        concurrent: bool = True,
    ) -> List[Path]:
        """
        Convert multiple texts to speech and save to files in batch (async).
        
        Args:
            texts: List of texts to convert to speech
            output_dir: Directory where audio files will be saved
            filename_prefix: Prefix for generated filenames (default: 'audio')
            voice: Voice character to use for all texts
            response_format: Audio format for all outputs
            concurrent: If True, process requests concurrently
            
        Returns:
            List[Path]: List of paths to the saved audio files
        """
        import asyncio
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Determine file extension
        fmt = response_format
        if isinstance(fmt, AudioFormat):
            ext = fmt.value
        elif fmt is not None:
            ext = str(fmt)
        else:
            ext = "mp3"
        
        if concurrent:
            tasks = [
                self.text_to_speech_file(
                    text=text,
                    output_path=output_dir / f"{filename_prefix}_{i}.{ext}",
                    voice=voice,
                    response_format=response_format,
                )
                for i, text in enumerate(texts)
            ]
            return await asyncio.gather(*tasks)
        else:
            results = []
            for i, text in enumerate(texts):
                path = await self.text_to_speech_file(
                    text=text,
                    output_path=output_dir / f"{filename_prefix}_{i}.{ext}",
                    voice=voice,
                    response_format=response_format,
                )
                results.append(path)
            return results

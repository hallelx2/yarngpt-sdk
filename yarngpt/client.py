"""YarnGPT API Client."""

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
        self, api_key: Optional[str] = None, base_url: Optional[str] = None, timeout: float = 30.0
    ):
        """Initialize the YarnGPT client."""
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
            elif response.status_code == 429:
                # Rate limit or quota exceeded
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
                # Payment required
                raise PaymentRequiredError(
                    "Payment required. Please check your account balance or subscription."
                )
            elif response.status_code == 403:
                # Forbidden
                raise AuthenticationError(
                    "Access forbidden. Please check your API key permissions."
                )
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

    def batch_text_to_speech(
        self,
        texts: List[str],
        voice: Optional[Union[Voice, str]] = None,
        response_format: Optional[Union[AudioFormat, str]] = None,
    ) -> List[bytes]:
        """
        Convert multiple texts to speech in batch.

        Args:
            texts: List of texts to convert to speech (each max 2000 characters)
            voice: Voice character to use for all texts (defaults to 'Idera')
            response_format: Audio format for all outputs (defaults to mp3)

        Returns:
            List[bytes]: List of audio data in the requested format

        Raises:
            ValidationError: If any text is invalid
            AuthenticationError: If API key is invalid
            APIError: If any API request fails

        Example:
            >>> client = YarnGPT()
            >>> texts = ["Hello", "Welcome", "Goodbye"]
            >>> audios = client.batch_text_to_speech(texts, voice=Voice.IDERA)
            >>> for i, audio in enumerate(audios):
            ...     with open(f"output_{i}.mp3", "wb") as f:
            ...         f.write(audio)
        """
        results = []
        for text in texts:
            audio = self.text_to_speech(
                text=text,
                voice=voice,
                response_format=response_format,
            )
            results.append(audio)
        return results

    def batch_text_to_speech_files(
        self,
        texts: List[str],
        output_dir: Union[str, Path],
        filename_prefix: str = "audio",
        voice: Optional[Union[Voice, str]] = None,
        response_format: Optional[Union[AudioFormat, str]] = None,
    ) -> List[Path]:
        """
        Convert multiple texts to speech and save to files in batch.

        Args:
            texts: List of texts to convert to speech (each max 2000 characters)
            output_dir: Directory where audio files will be saved
            filename_prefix: Prefix for generated filenames (default: 'audio')
            voice: Voice character to use for all texts (defaults to 'Idera')
            response_format: Audio format for all outputs (defaults to mp3)

        Returns:
            List[Path]: List of paths to the saved audio files

        Example:
            >>> client = YarnGPT()
            >>> texts = ["First text", "Second text", "Third text"]
            >>> paths = client.batch_text_to_speech_files(
            ...     texts,
            ...     "output",
            ...     voice=Voice.EMMA
            ... )
            >>> # Creates: output/audio_0.mp3, output/audio_1.mp3, output/audio_2.mp3
        """
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

        results = []
        for i, text in enumerate(texts):
            output_path = output_dir / f"{filename_prefix}_{i}.{ext}"
            path = self.text_to_speech_file(
                text=text,
                output_path=output_path,
                voice=voice,
                response_format=response_format,
            )
            results.append(path)

        return results

    def batch_text_to_speech_dict(
        self,
        text_dict: Dict[str, str],
        output_dir: Union[str, Path],
        voice: Optional[Union[Voice, str]] = None,
        response_format: Optional[Union[AudioFormat, str]] = None,
    ) -> Dict[str, Path]:
        """
        Convert multiple texts to speech using custom filenames from a dictionary.

        Args:
            text_dict: Dictionary mapping filenames (without extension) to texts
            output_dir: Directory where audio files will be saved
            voice: Voice character to use for all texts (defaults to 'Idera')
            response_format: Audio format for all outputs (defaults to mp3)

        Returns:
            Dict[str, Path]: Dictionary mapping original keys to saved file paths

        Example:
            >>> client = YarnGPT()
            >>> texts = {
            ...     "greeting": "Hello, welcome!",
            ...     "farewell": "Goodbye, see you!",
            ...     "thanks": "Thank you very much!"
            ... }
            >>> paths = client.batch_text_to_speech_dict(
            ...     texts,
            ...     "audio_output",
            ...     voice=Voice.JUDE
            ... )
            >>> # Creates: greeting.mp3, farewell.mp3, thanks.mp3
        """
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

        results = {}
        for filename, text in text_dict.items():
            output_path = output_dir / f"{filename}.{ext}"
            path = self.text_to_speech_file(
                text=text,
                output_path=output_path,
                voice=voice,
                response_format=response_format,
            )
            results[filename] = path

        return results

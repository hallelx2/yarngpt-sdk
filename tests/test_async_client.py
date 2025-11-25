"""Tests for AsyncYarnGPT client."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx

from yarngpt import AsyncYarnGPT, Voice, AudioFormat, RetryConfig
from yarngpt.exceptions import (
    AuthenticationError,
    ValidationError,
    QuotaExceededError,
)


@pytest.fixture
def mock_api_key():
    """Provide a mock API key."""
    return "test_api_key_12345"


@pytest.fixture
def mock_audio_data():
    """Provide mock audio data."""
    return b"fake_audio_data_content"


@pytest.mark.asyncio
async def test_async_client_initialization(mock_api_key):
    """Test AsyncYarnGPT client initialization."""
    async with AsyncYarnGPT(api_key=mock_api_key) as client:
        assert client.api_key == mock_api_key
        assert client.base_url == AsyncYarnGPT.DEFAULT_BASE_URL
        assert client.timeout == 30.0
        assert isinstance(client.retry_config, RetryConfig)


@pytest.mark.asyncio
async def test_async_client_no_api_key():
    """Test AsyncYarnGPT raises error without API key."""
    with patch("yarngpt.async_client.config", return_value=""):
        with pytest.raises(AuthenticationError):
            async with AsyncYarnGPT(api_key=None):
                pass


@pytest.mark.asyncio
async def test_async_text_to_speech_success(mock_api_key, mock_audio_data):
    """Test successful async text-to-speech conversion."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = mock_audio_data

    with patch.object(httpx.AsyncClient, "post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response

        async with AsyncYarnGPT(api_key=mock_api_key) as client:
            audio = await client.text_to_speech(
                text="Hello, Nigeria!",
                voice=Voice.IDERA,
                response_format=AudioFormat.MP3,
            )

            assert audio == mock_audio_data
            mock_post.assert_called_once()


@pytest.mark.asyncio
async def test_async_text_to_speech_empty_text(mock_api_key):
    """Test async text-to-speech with empty text raises ValidationError."""
    async with AsyncYarnGPT(api_key=mock_api_key) as client:
        with pytest.raises(ValidationError, match="Text cannot be empty"):
            await client.text_to_speech(text="")


@pytest.mark.asyncio
async def test_async_text_to_speech_text_too_long(mock_api_key):
    """Test async text-to-speech with text exceeding max length."""
    long_text = "a" * 2001

    async with AsyncYarnGPT(api_key=mock_api_key) as client:
        with pytest.raises(ValidationError, match="exceeds maximum"):
            await client.text_to_speech(text=long_text)


@pytest.mark.asyncio
async def test_async_text_to_speech_invalid_api_key(mock_api_key):
    """Test async text-to-speech with invalid API key."""
    mock_response = MagicMock()
    mock_response.status_code = 401

    with patch.object(httpx.AsyncClient, "post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response

        async with AsyncYarnGPT(api_key=mock_api_key) as client:
            with pytest.raises(AuthenticationError, match="Invalid API key"):
                await client.text_to_speech(text="Test")


@pytest.mark.asyncio
async def test_async_text_to_speech_quota_exceeded(mock_api_key):
    """Test async text-to-speech with quota exceeded."""
    mock_response = MagicMock()
    mock_response.status_code = 429
    mock_response.json.return_value = {"error": "Quota exceeded"}

    with patch.object(httpx.AsyncClient, "post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response

        async with AsyncYarnGPT(api_key=mock_api_key) as client:
            with pytest.raises(QuotaExceededError, match="Quota exceeded"):
                await client.text_to_speech(text="Test")


@pytest.mark.asyncio
async def test_async_text_to_speech_file(mock_api_key, mock_audio_data, tmp_path):
    """Test async text-to-speech saving to file."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = mock_audio_data

    output_file = tmp_path / "test_output.mp3"

    with patch.object(httpx.AsyncClient, "post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response

        async with AsyncYarnGPT(api_key=mock_api_key) as client:
            result_path = await client.text_to_speech_file(
                text="Test audio",
                output_path=output_file,
                voice=Voice.EMMA,
            )

            assert result_path == output_file
            assert output_file.exists()
            assert output_file.read_bytes() == mock_audio_data


@pytest.mark.asyncio
async def test_async_batch_text_to_speech_sequential(mock_api_key, mock_audio_data):
    """Test async batch conversion (sequential)."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = mock_audio_data

    texts = ["Hello", "Welcome", "Goodbye"]

    with patch.object(httpx.AsyncClient, "post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response

        async with AsyncYarnGPT(api_key=mock_api_key) as client:
            results = await client.batch_text_to_speech(
                texts=texts,
                concurrent=False,
            )

            assert len(results) == len(texts)
            assert all(audio == mock_audio_data for audio in results)
            assert mock_post.call_count == len(texts)


@pytest.mark.asyncio
async def test_async_batch_text_to_speech_concurrent(mock_api_key, mock_audio_data):
    """Test async batch conversion (concurrent)."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = mock_audio_data

    texts = ["Hello", "Welcome", "Goodbye"]

    with patch.object(httpx.AsyncClient, "post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response

        async with AsyncYarnGPT(api_key=mock_api_key) as client:
            results = await client.batch_text_to_speech(
                texts=texts,
                concurrent=True,
            )

            assert len(results) == len(texts)
            assert all(audio == mock_audio_data for audio in results)
            assert mock_post.call_count == len(texts)


@pytest.mark.asyncio
async def test_async_batch_text_to_speech_files(mock_api_key, mock_audio_data, tmp_path):
    """Test async batch conversion to files."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = mock_audio_data

    texts = ["First", "Second", "Third"]
    output_dir = tmp_path / "audio_output"

    with patch.object(httpx.AsyncClient, "post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response

        async with AsyncYarnGPT(api_key=mock_api_key) as client:
            paths = await client.batch_text_to_speech_files(
                texts=texts,
                output_dir=output_dir,
                filename_prefix="test",
                concurrent=True,
            )

            assert len(paths) == len(texts)
            assert all(path.exists() for path in paths)
            assert all(path.read_bytes() == mock_audio_data for path in paths)


@pytest.mark.asyncio
async def test_async_context_manager(mock_api_key):
    """Test async context manager properly closes client."""
    client = AsyncYarnGPT(api_key=mock_api_key)

    async with client:
        assert client._client is not None

    assert client._client is None


@pytest.mark.asyncio
async def test_async_custom_retry_config(mock_api_key):
    """Test async client with custom retry configuration."""
    retry_config = RetryConfig(max_retries=5, backoff_factor=3.0)

    async with AsyncYarnGPT(api_key=mock_api_key, retry_config=retry_config) as client:
        assert client.retry_config.max_retries == 5
        assert client.retry_config.backoff_factor == 3.0


@pytest.mark.asyncio
async def test_async_timeout_configuration(mock_api_key):
    """Test async client with custom timeout."""
    timeout = 60.0

    async with AsyncYarnGPT(api_key=mock_api_key, timeout=timeout) as client:
        assert client.timeout == timeout


@pytest.mark.asyncio
@pytest.mark.integration
async def test_async_integration_real_api():
    """Integration test with real API (requires YARNGPT_API_KEY)."""
    import os

    api_key = os.getenv("YARNGPT_API_KEY")
    if not api_key:
        pytest.skip("YARNGPT_API_KEY not set")

    async with AsyncYarnGPT(api_key=api_key) as client:
        audio = await client.text_to_speech(
            text="Integration test from async client",
            voice=Voice.IDERA,
            response_format=AudioFormat.MP3,
        )

        assert isinstance(audio, bytes)
        assert len(audio) > 0

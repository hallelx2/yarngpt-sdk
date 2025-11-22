"""Unit tests for YarnGPT SDK."""

import pytest
from pathlib import Path
from yarngpt import YarnGPT, Voice, AudioFormat
from yarngpt.exceptions import (
    AuthenticationError,
    ValidationError,
    APIError,
    YarnGPTError
)


class TestYarnGPTInit:
    """Test YarnGPT initialization."""
    
    def test_init_with_api_key(self):
        """Test initialization with valid API key."""
        client = YarnGPT(api_key="test_key")
        assert client.api_key == "test_key"
        assert client.base_url == YarnGPT.DEFAULT_BASE_URL
        assert client.timeout == 30.0
        client.close()
    
    def test_init_without_api_key(self):
        """Test initialization without API key raises error."""
        with pytest.raises(AuthenticationError):
            YarnGPT(api_key="")
    
    def test_init_with_custom_base_url(self):
        """Test initialization with custom base URL."""
        client = YarnGPT(api_key="test_key", base_url="https://custom.api")
        assert client.base_url == "https://custom.api"
        client.close()
    
    def test_context_manager(self):
        """Test context manager usage."""
        with YarnGPT(api_key="test_key") as client:
            assert client.api_key == "test_key"


class TestVoiceEnum:
    """Test Voice enum."""
    
    def test_all_voices_have_values(self):
        """Test all voices have string values."""
        for voice in Voice:
            assert isinstance(voice.value, str)
            assert len(voice.value) > 0
    
    def test_voice_descriptions(self):
        """Test voice descriptions."""
        assert Voice.IDERA.description == "Melodic, gentle"
        assert Voice.EMMA.description == "Authoritative, deep"
        assert Voice.ADAM.description == "Deep, clear"
    
    def test_voice_count(self):
        """Test we have all 16 voices."""
        assert len(list(Voice)) == 16


class TestAudioFormatEnum:
    """Test AudioFormat enum."""
    
    def test_audio_formats(self):
        """Test audio format values."""
        assert AudioFormat.MP3.value == "mp3"
        assert AudioFormat.WAV.value == "wav"
        assert AudioFormat.OPUS.value == "opus"
        assert AudioFormat.FLAC.value == "flac"
    
    def test_format_count(self):
        """Test we have all 4 formats."""
        assert len(list(AudioFormat)) == 4


class TestTextToSpeechValidation:
    """Test text-to-speech input validation."""
    
    def test_empty_text_raises_error(self):
        """Test empty text raises ValidationError."""
        client = YarnGPT(api_key="test_key")
        with pytest.raises(ValidationError, match="Text cannot be empty"):
            client.text_to_speech("")
        client.close()
    
    def test_text_too_long_raises_error(self):
        """Test text exceeding max length raises ValidationError."""
        client = YarnGPT(api_key="test_key")
        long_text = "A" * 2001
        with pytest.raises(ValidationError, match="exceeds maximum"):
            client.text_to_speech(long_text)
        client.close()
    
    def test_max_length_text_accepted(self):
        """Test text at max length is accepted."""
        client = YarnGPT(api_key="test_key")
        max_text = "A" * 2000
        # This will fail at API call, but should pass validation
        try:
            client.text_to_speech(max_text)
        except (APIError, AuthenticationError):
            pass  # Expected to fail at API level with test key
        client.close()


class TestExceptions:
    """Test exception hierarchy."""
    
    def test_exception_inheritance(self):
        """Test exception inheritance chain."""
        assert issubclass(AuthenticationError, YarnGPTError)
        assert issubclass(ValidationError, YarnGPTError)
        assert issubclass(APIError, YarnGPTError)
        assert issubclass(YarnGPTError, Exception)
    
    def test_exception_messages(self):
        """Test exceptions can be raised with messages."""
        with pytest.raises(ValidationError, match="Test error"):
            raise ValidationError("Test error")


class TestIntegration:
    """Integration tests (require valid API key from .env)."""
    
    @pytest.mark.integration
    def test_real_tts_request(self):
        """Test real TTS request with API key from .env file."""
        with YarnGPT() as client:
            audio = client.text_to_speech(
                text="Test speech",
                voice=Voice.IDERA
            )
            assert isinstance(audio, bytes)
            assert len(audio) > 0
    
    @pytest.mark.integration
    def test_save_to_file(self, tmp_path):
        """Test saving audio to file with API key from .env file."""
        output_file = tmp_path / "test_output.mp3"
        
        with YarnGPT() as client:
            result_path = client.text_to_speech_file(
                text="Test speech",
                output_path=output_file,
                voice=Voice.JUDE
            )
            
            assert result_path.exists()
            assert result_path.stat().st_size > 0

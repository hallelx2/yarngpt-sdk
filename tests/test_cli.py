"""Tests for CLI commands."""

import pytest
from pathlib import Path
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock

from yarngpt.cli import app
from yarngpt import Voice, AudioFormat


runner = CliRunner()


@pytest.fixture
def mock_audio_data():
    """Provide mock audio data."""
    return b"fake_audio_content"


@pytest.fixture
def mock_client(mock_audio_data):
    """Provide a mocked YarnGPT client."""
    with patch("yarngpt.cli.YarnGPT") as MockClient:
        client_instance = MagicMock()
        client_instance.text_to_speech.return_value = mock_audio_data
        client_instance.batch_text_to_speech_files.return_value = [
            Path("output/audio_0.mp3"),
            Path("output/audio_1.mp3"),
        ]
        MockClient.return_value = client_instance
        yield MockClient


def test_cli_no_args_shows_banner():
    """Test CLI without arguments shows welcome banner."""
    result = runner.invoke(app, [])
    
    assert result.exit_code == 0
    assert "YARNGPT" in result.stdout or "YarnGPT" in result.stdout
    assert "Nigerian" in result.stdout
    assert "convert" in result.stdout
    assert "batch" in result.stdout


def test_cli_help_shows_banner():
    """Test CLI --help shows banner."""
    result = runner.invoke(app, ["--help"])
    
    assert result.exit_code == 0
    assert "Usage:" in result.stdout
    assert "Commands" in result.stdout


def test_cli_convert_command_basic(mock_client, mock_audio_data, tmp_path):
    """Test basic convert command."""
    output_file = tmp_path / "output.mp3"
    
    with patch("yarngpt.cli.open", create=True) as mock_open:
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        result = runner.invoke(app, [
            "convert",
            "Hello Nigeria",
            "--output", str(output_file),
            "--api-key", "test_key",
        ])
        
        assert result.exit_code == 0
        assert "Success" in result.stdout
        mock_client.return_value.text_to_speech.assert_called_once()


def test_cli_convert_command_with_voice(mock_client, tmp_path):
    """Test convert command with specific voice."""
    output_file = tmp_path / "output.mp3"
    
    with patch("yarngpt.cli.open", create=True):
        result = runner.invoke(app, [
            "convert",
            "Test message",
            "--output", str(output_file),
            "--voice", "emma",
            "--api-key", "test_key",
        ])
        
        assert result.exit_code == 0
        call_args = mock_client.return_value.text_to_speech.call_args
        assert call_args[1]["voice"] == Voice.EMMA


def test_cli_convert_command_with_format(mock_client, tmp_path):
    """Test convert command with specific format."""
    output_file = tmp_path / "output.wav"
    
    with patch("yarngpt.cli.open", create=True):
        result = runner.invoke(app, [
            "convert",
            "Test audio",
            "--output", str(output_file),
            "--format", "wav",
            "--api-key", "test_key",
        ])
        
        assert result.exit_code == 0
        call_args = mock_client.return_value.text_to_speech.call_args
        assert call_args[1]["response_format"] == AudioFormat.WAV


def test_cli_convert_command_invalid_voice(mock_client, tmp_path):
    """Test convert command with invalid voice name."""
    output_file = tmp_path / "output.mp3"
    
    result = runner.invoke(app, [
        "convert",
        "Test",
        "--output", str(output_file),
        "--voice", "invalid_voice",
        "--api-key", "test_key",
    ])
    
    assert result.exit_code == 1
    assert "Invalid voice" in result.stdout


def test_cli_convert_command_invalid_format(mock_client, tmp_path):
    """Test convert command with invalid format."""
    output_file = tmp_path / "output.mp3"
    
    result = runner.invoke(app, [
        "convert",
        "Test",
        "--output", str(output_file),
        "--format", "invalid_format",
        "--api-key", "test_key",
    ])
    
    assert result.exit_code == 1
    assert "Invalid format" in result.stdout


def test_cli_convert_command_no_api_key():
    """Test convert command without API key."""
    with patch("yarngpt.cli.YarnGPT") as MockClient:
        MockClient.side_effect = Exception("API key required")
        
        result = runner.invoke(app, [
            "convert",
            "Test",
        ])
        
        assert result.exit_code == 1


def test_cli_batch_command_text_file(mock_client, tmp_path):
    """Test batch command with text file."""
    input_file = tmp_path / "texts.txt"
    input_file.write_text("Hello\nWelcome\nGoodbye\n")
    
    result = runner.invoke(app, [
        "batch",
        str(input_file),
        "--output-dir", "output",
        "--api-key", "test_key",
    ])
    
    assert result.exit_code == 0
    assert "Success" in result.stdout
    mock_client.return_value.batch_text_to_speech_files.assert_called_once()


def test_cli_batch_command_json_file(mock_client, tmp_path):
    """Test batch command with JSON file."""
    import json
    
    input_file = tmp_path / "texts.json"
    input_file.write_text(json.dumps(["Hello", "Welcome", "Goodbye"]))
    
    result = runner.invoke(app, [
        "batch",
        str(input_file),
        "--output-dir", "output",
        "--api-key", "test_key",
    ])
    
    assert result.exit_code == 0
    mock_client.return_value.batch_text_to_speech_files.assert_called_once()


def test_cli_batch_command_file_not_found():
    """Test batch command with non-existent file."""
    result = runner.invoke(app, [
        "batch",
        "nonexistent.txt",
        "--api-key", "test_key",
    ])
    
    assert result.exit_code == 1
    assert "File not found" in result.stdout


def test_cli_batch_command_empty_file(mock_client, tmp_path):
    """Test batch command with empty file."""
    input_file = tmp_path / "empty.txt"
    input_file.write_text("")
    
    result = runner.invoke(app, [
        "batch",
        str(input_file),
        "--api-key", "test_key",
    ])
    
    assert result.exit_code == 1
    assert "No texts found" in result.stdout


def test_cli_batch_command_with_options(mock_client, tmp_path):
    """Test batch command with custom options."""
    input_file = tmp_path / "texts.txt"
    input_file.write_text("Test1\nTest2\n")
    
    result = runner.invoke(app, [
        "batch",
        str(input_file),
        "--output-dir", "custom_output",
        "--prefix", "speech",
        "--voice", "jude",
        "--format", "wav",
        "--api-key", "test_key",
    ])
    
    assert result.exit_code == 0
    call_args = mock_client.return_value.batch_text_to_speech_files.call_args
    assert call_args[1]["output_dir"] == Path("custom_output")
    assert call_args[1]["filename_prefix"] == "speech"
    assert call_args[1]["voice"] == Voice.JUDE
    assert call_args[1]["response_format"] == AudioFormat.WAV


def test_cli_voices_command():
    """Test voices command lists all voices."""
    result = runner.invoke(app, ["voices"])
    
    assert result.exit_code == 0
    assert "Available" in result.stdout or "Voices" in result.stdout
    assert "Idera" in result.stdout
    assert "Emma" in result.stdout
    assert "Jude" in result.stdout


def test_cli_formats_command():
    """Test formats command lists all formats."""
    result = runner.invoke(app, ["formats"])
    
    assert result.exit_code == 0
    assert "Supported" in result.stdout or "Formats" in result.stdout
    assert "mp3" in result.stdout.lower()
    assert "wav" in result.stdout.lower()
    assert "opus" in result.stdout.lower()
    assert "flac" in result.stdout.lower()


def test_cli_version_command():
    """Test version command shows SDK version."""
    result = runner.invoke(app, ["version"])
    
    assert result.exit_code == 0
    assert "version" in result.stdout.lower()
    # Check for version pattern
    assert "0." in result.stdout


def test_cli_info_command():
    """Test info command shows API information."""
    result = runner.invoke(app, ["info"])
    
    assert result.exit_code == 0
    assert "Information" in result.stdout or "API" in result.stdout
    assert "80" in result.stdout  # Free tier limit
    assert "2,000" in result.stdout or "2000" in result.stdout  # Max text length
    assert "https://yarngpt.ai" in result.stdout


def test_cli_convert_with_env_api_key(mock_client, tmp_path):
    """Test convert command uses environment variable for API key."""
    output_file = tmp_path / "output.mp3"
    
    with patch("yarngpt.cli.open", create=True):
        with patch.dict("os.environ", {"YARNGPT_API_KEY": "env_test_key"}):
            result = runner.invoke(app, [
                "convert",
                "Test",
                "--output", str(output_file),
            ])
            
            # Should succeed without explicit --api-key
            assert result.exit_code == 0


def test_cli_convert_handles_quota_exceeded(tmp_path):
    """Test convert command handles quota exceeded error."""
    from yarngpt.exceptions import QuotaExceededError
    
    output_file = tmp_path / "output.mp3"
    
    with patch("yarngpt.cli.YarnGPT") as MockClient:
        client_instance = MagicMock()
        client_instance.text_to_speech.side_effect = QuotaExceededError("Quota exceeded")
        MockClient.return_value = client_instance
        
        result = runner.invoke(app, [
            "convert",
            "Test",
            "--output", str(output_file),
            "--api-key", "test_key",
        ])
        
        assert result.exit_code == 1
        assert "Quota Exceeded" in result.stdout
        assert "80" in result.stdout  # Mentions daily limit


def test_cli_convert_handles_validation_error(tmp_path):
    """Test convert command handles validation error."""
    from yarngpt.exceptions import ValidationError
    
    output_file = tmp_path / "output.mp3"
    
    with patch("yarngpt.cli.YarnGPT") as MockClient:
        client_instance = MagicMock()
        client_instance.text_to_speech.side_effect = ValidationError("Text too long")
        MockClient.return_value = client_instance
        
        result = runner.invoke(app, [
            "convert",
            "Test",
            "--output", str(output_file),
            "--api-key", "test_key",
        ])
        
        assert result.exit_code == 1
        assert "Validation Error" in result.stdout

# YarnGPT Python SDK

[![Tests](https://github.com/hallelx2/yarngpt-sdk/actions/workflows/test.yml/badge.svg)](https://github.com/hallelx2/yarngpt-sdk/actions/workflows/test.yml)
[![Code Quality](https://github.com/hallelx2/yarngpt-sdk/actions/workflows/lint.yml/badge.svg)](https://github.com/hallelx2/yarngpt-sdk/actions/workflows/lint.yml)
[![PyPI version](https://badge.fury.io/py/yarngpt-sdk.svg)](https://badge.fury.io/py/yarngpt-sdk)
[![Python Support](https://img.shields.io/pypi/pyversions/yarngpt-sdk.svg)](https://pypi.org/project/yarngpt-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Unofficial community-built Python SDK for [YarnGPT](https://yarngpt.ai) - A powerful Text-to-Speech API featuring authentic Nigerian accents.

> **Note:** This is a community-maintained SDK and is not officially endorsed by YarnGPT. For official support, please visit [yarngpt.ai](https://yarngpt.ai).

## Features

- 🎤 **16 Unique Nigerian Voices** - Choose from a diverse range of authentic accents
- 🔊 **Multiple Audio Formats** - Support for MP3, WAV, OPUS, and FLAC
- 🚀 **Simple & Intuitive API** - Get started in minutes
- 🔒 **Type-Safe** - Full type hints and enums for better IDE support
- ⚡ **Async Support** - Efficient for high-volume applications
- 📝 **Comprehensive Documentation** - Clear examples and API reference

## Installation

### Basic Installation

```bash
pip install yarngpt-sdk
```

### With CLI Support

```bash
# Install with command-line interface
pip install yarngpt-sdk[cli]
```

### Development Installation

```bash
# Install with development dependencies
pip install yarngpt-sdk[dev]

# Install everything (CLI + dev tools)
pip install yarngpt-sdk[cli,dev]
```

## Quick Start

### Python API

```python
from yarngpt import YarnGPT, Voice, AudioFormat

# Initialize the client with your API key
client = YarnGPT(api_key="your_api_key_here")

# Generate speech
audio = client.text_to_speech(
    text="Hello! Welcome to Nigeria.",
    voice=Voice.IDERA,
    response_format=AudioFormat.MP3
)

# Save to file
with open("output.mp3", "wb") as f:
    f.write(audio)
```

### Command-Line Interface

```bash
# Set your API key
export YARNGPT_API_KEY="your_api_key_here"

# Convert text to speech
yarngpt convert "Hello, welcome to Nigeria!"

# Specify voice and format
yarngpt convert "Good morning!" --voice emma --format wav -o greeting.wav

# Batch convert from a file
yarngpt batch texts.txt --output-dir audio_files --voice jude

# List all available voices
yarngpt voices

# Show API information
yarngpt info
```

## Authentication

Get your API key from your [YarnGPT Account Page](https://yarngpt.ai/account).

### Python API

```python
from yarngpt import YarnGPT

# Method 1: Pass directly
client = YarnGPT(api_key="your_api_key")

# Method 2: Use environment variable
import os
client = YarnGPT(api_key=os.getenv("YARNGPT_API_KEY"))

# Method 3: Auto-load from .env file
# Create .env file with: YARNGPT_API_KEY=your_api_key
client = YarnGPT()  # Automatically loads from environment
```

### CLI

```bash
# Method 1: Set environment variable
export YARNGPT_API_KEY="your_api_key"  # Linux/Mac
set YARNGPT_API_KEY=your_api_key       # Windows CMD
$env:YARNGPT_API_KEY="your_api_key"    # Windows PowerShell

# Method 2: Pass via command line
yarngpt convert "Hello" --api-key your_api_key

# Method 3: Use .env file
# Create .env file in your project directory
echo "YARNGPT_API_KEY=your_api_key" > .env
```

## Available Voices

The SDK provides 16 authentic Nigerian voices, each with unique characteristics:

| Voice Name | Description | Enum |
|-----------|-------------|------|
| Idera | Melodic, gentle | `Voice.IDERA` |
| Emma | Authoritative, deep | `Voice.EMMA` |
| Zainab | Soothing, gentle | `Voice.ZAINAB` |
| Osagie | Smooth, calm | `Voice.OSAGIE` |
| Wura | Young, sweet | `Voice.WURA` |
| Jude | Warm, confident | `Voice.JUDE` |
| Chinenye | Engaging, warm | `Voice.CHINENYE` |
| Tayo | Upbeat, energetic | `Voice.TAYO` |
| Regina | Mature, warm | `Voice.REGINA` |
| Femi | Rich, reassuring | `Voice.FEMI` |
| Adaora | Warm, engaging | `Voice.ADAORA` |
| Umar | Calm, smooth | `Voice.UMAR` |
| Mary | Energetic, youthful | `Voice.MARY` |
| Nonso | Bold, resonant | `Voice.NONSO` |
| Remi | Melodious, warm | `Voice.REMI` |
| Adam | Deep, clear | `Voice.ADAM` |

## Usage Examples

### Basic Text-to-Speech

```python
from yarngpt import YarnGPT, Voice

client = YarnGPT(api_key="your_api_key")

# Simple conversion
audio = client.text_to_speech("Hello, how are you doing today?")

# With specific voice
audio = client.text_to_speech(
    text="Welcome to our platform!",
    voice=Voice.EMMA
)
```

### Save Directly to File

```python
from yarngpt import YarnGPT, Voice, AudioFormat

client = YarnGPT(api_key="your_api_key")

# Save to file in one step
output_path = client.text_to_speech_file(
    text="This will be saved directly to a file",
    output_path="speech.mp3",
    voice=Voice.JUDE,
    response_format=AudioFormat.MP3
)

print(f"Audio saved to: {output_path}")
```

### Using Different Audio Formats

```python
from yarngpt import YarnGPT, AudioFormat

client = YarnGPT(api_key="your_api_key")

# Generate WAV format
audio_wav = client.text_to_speech(
    text="High quality audio",
    response_format=AudioFormat.WAV
)

# Generate OPUS format (good for streaming)
audio_opus = client.text_to_speech(
    text="Compressed audio",
    response_format=AudioFormat.OPUS
)
```

### Context Manager (Recommended)

```python
from yarngpt import YarnGPT, Voice

# Automatically handles cleanup
with YarnGPT(api_key="your_api_key") as client:
    audio = client.text_to_speech(
        text="Using context manager for proper resource management",
        voice=Voice.ADAORA
    )
    
    with open("output.mp3", "wb") as f:
        f.write(audio)
```

### Error Handling

```python
from yarngpt import YarnGPT, Voice
from yarngpt.exceptions import (
    AuthenticationError,
    ValidationError,
    APIError,
    QuotaExceededError,
    PaymentRequiredError,
    YarnGPTError
)

client = YarnGPT()

try:
    audio = client.text_to_speech(
        text="Your text here",
        voice=Voice.IDERA
    )
except QuotaExceededError as e:
    print(f"Quota exceeded: {e}")
    print("Free tier: 80 TTS requests/day")
except AuthenticationError:
    print("Invalid API key!")
except ValidationError as e:
    print(f"Invalid parameters: {e}")
except PaymentRequiredError as e:
    print(f"Payment required: {e}")
except APIError as e:
    print(f"API request failed: {e}")
except YarnGPTError as e:
    print(f"YarnGPT error: {e}")
```

### Daily Usage Limits

YarnGPT enforces the following daily limits:

| Resource | Free Tier Limit |
|----------|----------------|
| **TTS Requests** | 80/day |
| Media Processing Jobs | 8/day |
| URL Extractions | 100/day |
| Chunked Audio Generations | 120/day |

When you exceed these limits, the SDK will raise a `QuotaExceededError`.

### Working with Long Text

```python
from yarngpt import YarnGPT

client = YarnGPT(api_key="your_api_key")

# Text must be under 2000 characters
long_text = "Your long text here..."

if len(long_text) > 2000:
    # Split into chunks
    chunks = [long_text[i:i+2000] for i in range(0, len(long_text), 2000)]
    
    for i, chunk in enumerate(chunks):
        audio = client.text_to_speech(chunk)
        with open(f"output_part_{i}.mp3", "wb") as f:
            f.write(audio)
else:
    audio = client.text_to_speech(long_text)
```

## Command-Line Interface (CLI)

The YarnGPT SDK includes a powerful CLI tool for easy text-to-speech conversion from the terminal.

### Installation

```bash
pip install yarngpt-sdk[cli]
```

### CLI Commands

#### `yarngpt convert`

Convert text to speech and save to a file.

```bash
# Basic usage
yarngpt convert "Hello, welcome to Nigeria!"

# Custom output file
yarngpt convert "Good morning" -o greeting.mp3

# Specify voice
yarngpt convert "Test message" --voice emma

# Specify format
yarngpt convert "High quality" --format wav -o output.wav

# All options
yarngpt convert "Complete example" \
  --output audio.mp3 \
  --voice jude \
  --format mp3 \
  --api-key your_key
```

**Options:**
- `-o, --output PATH` - Output file path (default: output.mp3)
- `-v, --voice TEXT` - Voice name (default: idera)
- `-f, --format TEXT` - Audio format: mp3, wav, opus, flac (default: mp3)
- `-k, --api-key TEXT` - YarnGPT API key (or use YARNGPT_API_KEY env var)

#### `yarngpt batch`

Batch convert multiple texts from a file.

```bash
# Create a text file with one text per line
cat > texts.txt << EOF
Hello, welcome!
How are you today?
Thank you very much!
EOF

# Batch convert
yarngpt batch texts.txt

# Custom output directory and prefix
yarngpt batch texts.txt -o audio_files --prefix speech

# With specific voice and format
yarngpt batch texts.txt --voice emma --format wav
```

**Options:**
- `-o, --output-dir PATH` - Output directory (default: output)
- `-v, --voice TEXT` - Voice for all files (default: idera)
- `-f, --format TEXT` - Audio format for all files (default: mp3)
- `-p, --prefix TEXT` - Filename prefix (default: audio)
- `-k, --api-key TEXT` - YarnGPT API key

**Input Formats:**

Text file (one per line):
```text
First text to convert
Second text to convert
Third text to convert
```

JSON file (array of strings):
```json
[
  "First text to convert",
  "Second text to convert",
  "Third text to convert"
]
```

#### `yarngpt voices`

List all available voices with descriptions.

```bash
yarngpt voices
```

Output:
```
┌────────────┬────────────┬──────────────────────────┐
│ Name       │ Value      │ Description              │
├────────────┼────────────┼──────────────────────────┤
│ IDERA      │ Idera      │ Melodic and gentle voice │
│ EMMA       │ Emma       │ Authoritative and deep   │
│ ...        │ ...        │ ...                      │
└────────────┴────────────┴──────────────────────────┘
```

#### `yarngpt formats`

List all supported audio formats.

```bash
yarngpt formats
```

#### `yarngpt info`

Show API information, limits, and helpful links.

```bash
yarngpt info
```

Output shows:
- Free tier limits
- Available features
- Useful links
- Getting started guide

#### `yarngpt version`

Show the SDK version.

```bash
yarngpt version
```

### CLI Examples

**Convert with Nigerian accent:**
```bash
yarngpt convert "Welcome to Lagos!" --voice tayo -o lagos.mp3
```

**Create multiple greetings:**
```bash
cat > greetings.txt << EOF
Good morning, have a great day!
Good afternoon, hope you're doing well!
Good evening, time to relax!
EOF

yarngpt batch greetings.txt -o greetings --prefix greeting --voice regina
# Creates: greetings/greeting_0.mp3, greetings/greeting_1.mp3, ...
```

**High-quality WAV output:**
```bash
yarngpt convert "Professional audio message" \
  --voice adam \
  --format wav \
  -o professional.wav
```

**Quick voice testing:**
```bash
# List all voices
yarngpt voices

# Test different voices
yarngpt convert "Testing Idera voice" --voice idera -o test_idera.mp3
yarngpt convert "Testing Emma voice" --voice emma -o test_emma.mp3
yarngpt convert "Testing Jude voice" --voice jude -o test_jude.mp3
```

## API Reference

### `YarnGPT`

Main client class for interacting with the YarnGPT API.

#### Constructor

```python
YarnGPT(api_key: str, base_url: Optional[str] = None, timeout: float = 30.0)
```

**Parameters:**

- `api_key` (str): Your YarnGPT API key
- `base_url` (str, optional): Custom API base URL
- `timeout` (float, optional): Request timeout in seconds (default: 30)

#### Methods

##### `text_to_speech()`

Convert text to speech.

```python
client.text_to_speech(
    text: str,
    voice: Optional[Union[Voice, str]] = None,
    response_format: Optional[Union[AudioFormat, str]] = None
) -> bytes
```

**Parameters:**

- `text` (str): Text to convert (max 2000 characters)
- `voice` (Voice | str, optional): Voice to use (default: Idera)
- `response_format` (AudioFormat | str, optional): Audio format (default: mp3)

**Returns:** Audio data as bytes

##### `text_to_speech_file()`

Convert text to speech and save to file.

```python
client.text_to_speech_file(
    text: str,
    output_path: Union[str, Path],
    voice: Optional[Union[Voice, str]] = None,
    response_format: Optional[Union[AudioFormat, str]] = None
) -> Path
```

**Parameters:**

- `text` (str): Text to convert (max 2000 characters)
- `output_path` (str | Path): Where to save the audio file
- `voice` (Voice | str, optional): Voice to use (default: Idera)
- `response_format` (AudioFormat | str, optional): Audio format (default: mp3)

**Returns:** Path to the saved file

### Enums

#### `Voice`

Available voice options: `IDERA`, `EMMA`, `ZAINAB`, `OSAGIE`, `WURA`, `JUDE`, `CHINENYE`, `TAYO`, `REGINA`, `FEMI`, `ADAORA`, `UMAR`, `MARY`, `NONSO`, `REMI`, `ADAM`

#### `AudioFormat`

Supported audio formats: `MP3`, `WAV`, `OPUS`, `FLAC`

### Exceptions

- `YarnGPTError` - Base exception for all SDK errors
- `AuthenticationError` - Invalid or missing API key
- `ValidationError` - Invalid request parameters
- `QuotaExceededError` - Daily quota exceeded (80 TTS requests/day on free tier)
- `PaymentRequiredError` - Payment required to continue
- `APIError` - General API request failure

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yarngpt/yarngpt-sdk.git
cd yarngpt-sdk

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/ -v
```

### Code Formatting

```bash
black yarngpt/
ruff check yarngpt/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Roadmap

We have exciting features planned for future releases! See our [ROADMAP.md](ROADMAP.md) for details on:

- 🔄 **Async Support** - AsyncYarnGPT for concurrent applications
- 🔁 **Retry Logic** - Automatic retry with exponential backoff
- 💾 **Caching** - Optional caching to reduce API calls
- 🎵 **Audio Utilities** - Audio processing, validation, and concatenation
- 📊 **Usage Analytics** - Track and export usage statistics
- 🧪 **Mock Client** - Testing without API calls
- And much more!

See the full [roadmap](ROADMAP.md) for planned features and timelines.

## Links

- **Website:** [https://yarngpt.ai](https://yarngpt.ai)
- **API Documentation:** [https://yarngpt.ai/api-docs](https://yarngpt.ai)
- **Account/API Keys:** [https://yarngpt.ai/account](https://yarngpt.ai/account)
- **GitHub:** [https://github.com/hallelx2/yarngpt-sdk](https://github.com/hallelx2/yarngpt-sdk)
- **PyPI:** [https://pypi.org/project/yarngpt-sdk/](https://pypi.org/project/yarngpt-sdk/)
- **Roadmap:** [ROADMAP.md](https://github.com/hallelx2/yarngpt-sdk/blob/master/ROADMAP.md)

## Support

For issues, questions, or contributions, please visit our [GitHub Issues](https://github.com/hallelx2/yarngpt-sdk/issues) page.

---

**Maintainer:** Halleluyah Darasimi Oludele ([@hallelx2](https://github.com/hallelx2))

*Unofficial community SDK • Not affiliated with YarnGPT*

Made with ❤️ for the Nigerian developer community

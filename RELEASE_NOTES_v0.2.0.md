# YarnGPT SDK v0.2.0 Release Notes

## 🚀 Major Features

### AsyncYarnGPT Client

Full async/await support for high-performance, concurrent text-to-speech operations. Perfect for web applications, batch processing, and high-volume TTS generation.

```python
import asyncio
from yarngpt import AsyncYarnGPT, Voice

async def generate():
    async with AsyncYarnGPT() as client:
        audio = await client.text_to_speech(
            text="Hello from async!",
            voice=Voice.IDERA
        )
        return audio

asyncio.run(generate())
```

**Performance:** 1.63x faster concurrent batch processing compared to sequential operations!

### Retry Logic & Resilience

Automatic retry with exponential backoff for transient API failures:

- Smart retry for errors: 429, 500, 502, 503, 504
- Configurable max retries, backoff factor, and jitter
- Graceful error handling with partial failure support

```python
from yarngpt import YarnGPT, RetryConfig

retry_config = RetryConfig(
    max_retries=5,
    backoff_factor=2.0,
    jitter=True
)

client = YarnGPT(retry_config=retry_config)
```

### Enhanced CLI

Beautiful Nigerian-themed CLI with green-white-green styling:

- `yarngpt version` - Show SDK version
- `yarngpt info` - Display API limits and helpful information
- `yarngpt voices` - List all 16 available voices
- `yarngpt formats` - Show supported audio formats
- Improved error messages and progress indicators

```bash
yarngpt convert "Welcome to Nigeria!" --voice tayo -o welcome.mp3
```

## 📊 Testing & Quality

- **82 Tests Total:** 74 unit tests + 8 async integration tests
- **100% Pass Rate:** All tests passing
- **Performance Verified:** Concurrent processing 1.63x faster
- **Code Quality:** All ruff checks passing

## 📚 Documentation

- **380+ lines** of comprehensive async documentation
- Error handling guide with graceful degradation patterns
- Performance comparison examples
- Web framework integration examples (FastAPI, Django)
- Complete CLI usage guide

## 🔧 What's Changed

### Added

- AsyncYarnGPT client with full async/await support
- Concurrent batch processing (`batch_text_to_speech` with `concurrent=True`)
- RetryConfig for configurable retry behavior
- Enhanced CLI commands (version, info, voices, formats)
- Web framework integration examples
- Comprehensive async test suite

### Improved

- Error handling across all clients
- Batch processing performance
- Type hints and documentation
- CLI output styling

### Fixed

- UTF-8 encoding in PowerShell scripts
- Connection cleanup in async client
- Error propagation in batch operations

## 📦 Installation

```bash
pip install yarngpt-sdk==0.2.0
```

Or upgrade from 0.1.0:

```bash
pip install --upgrade yarngpt-sdk
```

## 🔄 Upgrading from 0.1.0

**No breaking changes!** The synchronous `YarnGPT` client remains fully compatible. New async features are opt-in.

```python
# Your existing code still works
from yarngpt import YarnGPT
client = YarnGPT()
audio = client.text_to_speech("Hello")

# New async support available
from yarngpt import AsyncYarnGPT
async with AsyncYarnGPT() as client:
    audio = await client.text_to_speech("Hello")
```

## 🌟 Perfect For

- **Web Applications:** FastAPI, Django, Flask integrations
- **High-Volume TTS:** Concurrent batch processing
- **Production Deployments:** Automatic retry and error handling
- **Audio Processing:** Batch conversion with progress tracking

## 📖 Resources

- **Documentation:** <https://github.com/hallelx2/yarngpt-sdk#readme>
- **Changelog:** <https://github.com/hallelx2/yarngpt-sdk/blob/master/CHANGELOG.md>
- **Issues:** <https://github.com/hallelx2/yarngpt-sdk/issues>
- **PyPI:** <https://pypi.org/project/yarngpt-sdk/>

## 🙏 Thank You

Thank you to everyone who has been using YarnGPT SDK! This release represents a significant step forward in making Nigerian accent text-to-speech accessible and performant for production applications.

---

**Full Changelog:** <https://github.com/hallelx2/yarngpt-sdk/compare/v0.1.0...v0.2.0>

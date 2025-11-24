# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-11-24

### Added

#### Async Support

- **AsyncYarnGPT client** for high-performance concurrent operations
- Full async/await support for all text-to-speech operations
- `async with` context manager for proper resource cleanup
- Concurrent batch processing with significant performance gains (1.63x faster)
- `batch_text_to_speech()` with `concurrent=True` for parallel processing
- `batch_text_to_speech_files()` for concurrent file generation
- Integration examples for FastAPI and Django async views

#### Retry Logic & Resilience

- **RetryConfig** for configurable automatic retry behavior
- Exponential backoff with jitter to prevent thundering herd
- Smart retry for transient errors (429, 500, 502, 503, 504)
- Configurable max retries, backoff factor, and max backoff time
- Graceful error handling with partial failure support in batch operations

#### CLI Enhancements

- Styled output with Nigerian flag colors (green-white-green)
- `yarngpt version` - Show SDK version
- `yarngpt info` - Display API information and limits
- `yarngpt voices` - List all available voices with descriptions
- `yarngpt formats` - Show supported audio formats
- Improved error messages and user feedback
- Better batch processing with progress indicators

#### Documentation

- Comprehensive async client documentation with examples (380+ lines)
- Error handling guide with graceful degradation patterns
- Performance comparison examples (sequential vs concurrent)
- Web framework integration examples
- CLI usage guide with practical examples
- Async verification report with test results

#### Testing

- 8 comprehensive async integration tests
- Async test suite (`test_async.py`)
- CLI test script (`test.ps1`) for PowerShell
- 100% test pass rate (74 unit + 8 async tests)
- Performance benchmarking in tests

### Changed

- Updated README with extensive async documentation
- Improved error handling across all clients
- Enhanced batch processing performance
- Better type hints and documentation strings

### Fixed

- UTF-8 encoding in PowerShell test scripts
- Graceful handling of API format limitations (OPUS)
- Connection cleanup in async client
- Error propagation in batch operations

### Performance

- **1.63x faster** concurrent batch processing vs sequential
- Efficient HTTP connection pooling in AsyncYarnGPT
- Reduced API call overhead with smart retry logic

## [0.1.0] - 2025-11-22

### Initial Features

- Initial release of YarnGPT SDK
- Support for 16 Nigerian accent voices
- Text-to-speech conversion with multiple audio formats (MP3, WAV, OPUS, FLAC)
- Type-safe Voice and AudioFormat enums
- Comprehensive error handling with custom exceptions
- Context manager support for proper resource management
- `text_to_speech()` method for generating audio data
- `text_to_speech_file()` convenience method for saving directly to files
- Complete documentation and examples
- Unit tests with pytest
- MIT License

### Features

- Synchronous HTTP client using httpx
- Maximum text length validation (2000 characters)
- Bearer token authentication
- Configurable timeout and base URL
- Full type hints for IDE support

[0.1.0]: https://github.com/hallelx2/yarngpt-sdk/releases/tag/v0.1.0

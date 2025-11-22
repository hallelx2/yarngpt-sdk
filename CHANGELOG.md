# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-22

### Added
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

[0.1.0]: https://github.com/yarngpt/yarngpt-sdk/releases/tag/v0.1.0

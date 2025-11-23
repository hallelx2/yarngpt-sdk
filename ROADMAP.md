# YarnGPT SDK Roadmap

This document outlines planned improvements and features for the YarnGPT Python SDK.

## Week 1 (November 23-30, 2025) - Current Sprint

### ✅ Implemented

- [x] CLI tool with Typer for command-line usage
- [x] Basic text-to-speech conversion
- [x] Multiple audio format support
- [x] Batch processing capabilities

### 🚧 This Week (In Progress)

- [ ] Test CLI functionality thoroughly
- [ ] Add CLI examples to documentation
- [ ] Add CONTRIBUTING.md guide

## Week 2 (December 1-7, 2025)

### 📋 Priority Features

#### Async Support

- **Status:** Planned
- **Description:** Add async client for better performance in concurrent applications
- **Components:**
  - `AsyncYarnGPT` class with `httpx.AsyncClient`
  - Async versions of all methods (`async def text_to_speech_async()`)
  - Support for `asyncio.gather()` for concurrent batch processing
- **Use Case:** Web servers, high-volume applications, concurrent processing
- **Example:**

  ```python
  async with AsyncYarnGPT() as client:
      audio = await client.text_to_speech_async("Hello!")
  ```

#### Retry Logic & Rate Limiting

- **Description:** Automatic retry with exponential backoff for transient failures
- **Components:**
  - Configurable retry policy (max retries, backoff factor)
  - Built-in rate limiting to respect API quotas
  - Smart retry for specific error codes (429, 500, 502, 503, 504)
- **Example:**

  ```python
  client = YarnGPT(
      api_key="...",
      retry_config=RetryConfig(max_retries=3, backoff_factor=2)
  )
  ```

## Week 3 (December 8-14, 2025)

### 📋 Priority Features

#### Mock Client for Testing

- **Description:** Testing without API key
- **Components:**
  - MockYarnGPT class
  - Pre-generated sample audio responses
  - Usage tracking

#### CLI Enhancements

- Interactive mode for multiple conversions
- Configuration file support (`.yarngptrc`)
- Voice preview/samples

## Week 4 (December 15-21, 2025)

### 📋 Priority Features

#### Caching Layer

- **Status:** Planned
- **Description:** Optional caching to reduce API calls for identical requests
- **Components:**
  - In-memory cache (default)
  - File-based cache
  - Redis cache support (optional)
  - Configurable TTL and cache size
- **Benefits:** Cost savings, faster responses for repeated requests
- **Example:**

  ```python
  client = YarnGPT(
      api_key="...",
      cache_backend="file",
      cache_ttl=3600
  )
  ```

#### Audio Utilities

- In-memory cache (default)
- File-based cache
- Configurable TTL and cache size
- **Example:**

  ```python
  client = YarnGPT(api_key="...", cache_backend="file", cache_ttl=3600)
  ```

#### Audio Validation & Processing

- Audio validation (format, duration, bitrate)
- Audio metadata extraction
- Smart text chunking at sentence boundaries

## Future Sprints (January 2026+)

### Advanced Features

#### Enhanced Batch Processing

- Concurrent/parallel batch processing
- Progress callbacks and tracking
- Partial success handling (continue on failures)
- Rate limit aware batching

#### Audio Concatenation

- Merge multiple audio files
- Format conversion utilities
- Audio processing utilities

#### Usage Analytics & Monitoring

- Usage statistics (requests, characters, costs)
- Quota warnings (alert before hitting limits)
- Export to CSV/JSON
- Debug mode with detailed logging

#### Streaming Support (API Dependent)

- Stream audio as it's generated
- Real-time applications
- Reduced latency
- **Note:** Depends on YarnGPT API supporting streaming

#### Advanced Type Safety

- Pydantic models for validation
- Runtime validation
- Better error messages
- OpenAPI schema generation

## Sprint Goals Summary

- **Week 1 (Nov 23-30):** Documentation, CLI testing, CONTRIBUTING.md
- **Week 2 (Dec 1-7):** Async support, retry logic
- **Week 3 (Dec 8-14):** Mock client, CLI enhancements
- **Week 4 (Dec 15-21):** Caching, audio utilities
- **Future:** Advanced batch processing, analytics, streaming

## Community Help Wanted

Priority areas for contributions:

1. **Examples:** Framework integrations (Django, FastAPI, Flask)
2. **Documentation:** Tutorials, guides, blog posts
3. **Testing:** Edge cases, integration tests
4. **Async Implementation:** AsyncYarnGPT class

## Feedback & Suggestions

- Open an issue: [GitHub Issues](https://github.com/hallelx2/yarngpt-sdk/issues)
- Start a discussion: [GitHub Discussions](https://github.com/hallelx2/yarngpt-sdk/discussions)

---

**Last Updated:** November 23, 2025  
**Maintainer:** Halleluyah Darasimi Oludele ([@hallelx2](https://github.com/hallelx2))

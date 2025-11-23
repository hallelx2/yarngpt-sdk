"""Tests for retry logic and configuration."""

import pytest
import time
from unittest.mock import Mock, patch
import httpx

from yarngpt.retry import (
    RetryConfig,
    calculate_backoff,
    should_retry,
    with_retry,
    with_retry_async,
)
from yarngpt.exceptions import (
    AuthenticationError,
    QuotaExceededError,
    APIError,
)


def test_retry_config_defaults():
    """Test RetryConfig default values."""
    config = RetryConfig()
    
    assert config.max_retries == 3
    assert config.backoff_factor == 2.0
    assert config.max_backoff == 60.0
    assert config.retry_statuses == (429, 500, 502, 503, 504)
    assert config.jitter is True


def test_retry_config_custom_values():
    """Test RetryConfig with custom values."""
    config = RetryConfig(
        max_retries=5,
        backoff_factor=3.0,
        max_backoff=120.0,
        jitter=False,
    )
    
    assert config.max_retries == 5
    assert config.backoff_factor == 3.0
    assert config.max_backoff == 120.0
    assert config.jitter is False


def test_retry_config_validation_max_retries():
    """Test RetryConfig validation for max_retries."""
    with pytest.raises(ValueError, match="max_retries must be >= 0"):
        RetryConfig(max_retries=-1)


def test_retry_config_validation_backoff_factor():
    """Test RetryConfig validation for backoff_factor."""
    with pytest.raises(ValueError, match="backoff_factor must be >= 1"):
        RetryConfig(backoff_factor=0.5)


def test_retry_config_validation_max_backoff():
    """Test RetryConfig validation for max_backoff."""
    with pytest.raises(ValueError, match="max_backoff must be >= 0"):
        RetryConfig(max_backoff=-10)


def test_calculate_backoff_exponential():
    """Test exponential backoff calculation."""
    config = RetryConfig(backoff_factor=2.0, max_backoff=100, jitter=False)
    
    assert calculate_backoff(0, config) == 1.0  # 2^0
    assert calculate_backoff(1, config) == 2.0  # 2^1
    assert calculate_backoff(2, config) == 4.0  # 2^2
    assert calculate_backoff(3, config) == 8.0  # 2^3


def test_calculate_backoff_max_limit():
    """Test backoff respects max_backoff limit."""
    config = RetryConfig(backoff_factor=2.0, max_backoff=10.0, jitter=False)
    
    assert calculate_backoff(10, config) == 10.0  # Should cap at max_backoff


def test_calculate_backoff_with_jitter():
    """Test backoff with jitter adds randomness."""
    config = RetryConfig(backoff_factor=2.0, max_backoff=100, jitter=True)
    
    # With jitter, results should vary between 0.5x and 1.5x base
    backoff = calculate_backoff(2, config)  # Base would be 4.0
    assert 2.0 <= backoff <= 6.0  # 4.0 * (0.5 to 1.5)


def test_should_retry_exceeds_max_attempts():
    """Test should_retry returns False when max attempts exceeded."""
    config = RetryConfig(max_retries=3)
    exception = Exception("Test error")
    
    assert should_retry(exception, 0, config) is False  # At max
    assert should_retry(exception, 5, config) is False  # Beyond max


def test_should_retry_authentication_error():
    """Test should_retry returns False for AuthenticationError."""
    config = RetryConfig(max_retries=3)
    exception = AuthenticationError("Invalid API key")
    
    assert should_retry(exception, 0, config) is False


def test_should_retry_quota_exceeded_error():
    """Test should_retry returns False for QuotaExceededError."""
    config = RetryConfig(max_retries=3)
    exception = QuotaExceededError("Daily limit reached")
    
    assert should_retry(exception, 0, config) is False


def test_should_retry_network_errors():
    """Test should_retry returns True for network errors."""
    config = RetryConfig(max_retries=3)
    
    timeout_error = httpx.TimeoutException("Request timed out")
    assert should_retry(timeout_error, 0, config) is True
    
    network_error = httpx.NetworkError("Connection failed")
    assert should_retry(network_error, 0, config) is True


def test_should_retry_retryable_status_codes():
    """Test should_retry returns True for retryable HTTP status codes."""
    config = RetryConfig(max_retries=3)
    
    for status_code in [429, 500, 502, 503, 504]:
        mock_response = Mock()
        mock_response.status_code = status_code
        exception = httpx.HTTPStatusError(
            message=f"Status {status_code}",
            request=Mock(),
            response=mock_response,
        )
        assert should_retry(exception, 0, config) is True


def test_should_retry_non_retryable_status_code():
    """Test should_retry returns False for non-retryable status codes."""
    config = RetryConfig(max_retries=3)
    
    mock_response = Mock()
    mock_response.status_code = 400
    exception = httpx.HTTPStatusError(
        message="Bad request",
        request=Mock(),
        response=mock_response,
    )
    assert should_retry(exception, 0, config) is False


def test_with_retry_decorator_success():
    """Test with_retry decorator with successful function."""
    call_count = 0
    
    @with_retry(RetryConfig(max_retries=3))
    def test_func():
        nonlocal call_count
        call_count += 1
        return "success"
    
    result = test_func()
    assert result == "success"
    assert call_count == 1


def test_with_retry_decorator_succeeds_after_retries():
    """Test with_retry decorator succeeds after initial failures."""
    call_count = 0
    
    @with_retry(RetryConfig(max_retries=3, backoff_factor=1.1, jitter=False))
    def test_func():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise httpx.TimeoutException("Timeout")
        return "success"
    
    start_time = time.time()
    result = test_func()
    elapsed = time.time() - start_time
    
    assert result == "success"
    assert call_count == 3
    # Should have backoff delays: ~1.1^0 + 1.1^1 = ~2.1 seconds
    assert elapsed >= 2.0


def test_with_retry_decorator_exhausts_retries():
    """Test with_retry decorator exhausts retries and raises."""
    call_count = 0
    
    @with_retry(RetryConfig(max_retries=2, backoff_factor=1.1, jitter=False))
    def test_func():
        nonlocal call_count
        call_count += 1
        raise httpx.TimeoutException("Always fails")
    
    with pytest.raises(httpx.TimeoutException):
        test_func()
    
    assert call_count == 3  # Initial + 2 retries


def test_with_retry_decorator_no_retry_on_auth_error():
    """Test with_retry decorator doesn't retry AuthenticationError."""
    call_count = 0
    
    @with_retry(RetryConfig(max_retries=3))
    def test_func():
        nonlocal call_count
        call_count += 1
        raise AuthenticationError("Invalid key")
    
    with pytest.raises(AuthenticationError):
        test_func()
    
    assert call_count == 1  # No retries


@pytest.mark.asyncio
async def test_with_retry_async_decorator_success():
    """Test with_retry_async decorator with successful function."""
    call_count = 0
    
    @with_retry_async(RetryConfig(max_retries=3))
    async def test_func():
        nonlocal call_count
        call_count += 1
        return "success"
    
    result = await test_func()
    assert result == "success"
    assert call_count == 1


@pytest.mark.asyncio
async def test_with_retry_async_decorator_succeeds_after_retries():
    """Test with_retry_async decorator succeeds after initial failures."""
    call_count = 0
    
    @with_retry_async(RetryConfig(max_retries=3, backoff_factor=1.1, jitter=False))
    async def test_func():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise httpx.TimeoutException("Timeout")
        return "success"
    
    start_time = time.time()
    result = await test_func()
    elapsed = time.time() - start_time
    
    assert result == "success"
    assert call_count == 3
    assert elapsed >= 2.0


@pytest.mark.asyncio
async def test_with_retry_async_decorator_exhausts_retries():
    """Test with_retry_async decorator exhausts retries and raises."""
    call_count = 0
    
    @with_retry_async(RetryConfig(max_retries=2, backoff_factor=1.1, jitter=False))
    async def test_func():
        nonlocal call_count
        call_count += 1
        raise httpx.TimeoutException("Always fails")
    
    with pytest.raises(httpx.TimeoutException):
        await test_func()
    
    assert call_count == 3


@pytest.mark.asyncio
async def test_with_retry_async_decorator_no_retry_on_quota():
    """Test with_retry_async decorator doesn't retry QuotaExceededError."""
    call_count = 0
    
    @with_retry_async(RetryConfig(max_retries=3))
    async def test_func():
        nonlocal call_count
        call_count += 1
        raise QuotaExceededError("Daily limit")
    
    with pytest.raises(QuotaExceededError):
        await test_func()
    
    assert call_count == 1


def test_retry_with_different_backoff_factors():
    """Test retry behavior with different backoff factors."""
    for backoff_factor in [1.5, 2.0, 3.0]:
        config = RetryConfig(backoff_factor=backoff_factor, max_backoff=100, jitter=False)
        
        backoff_0 = calculate_backoff(0, config)
        backoff_1 = calculate_backoff(1, config)
        backoff_2 = calculate_backoff(2, config)
        
        assert backoff_0 == 1.0
        assert backoff_1 == backoff_factor
        assert backoff_2 == backoff_factor ** 2


def test_retry_config_custom_status_codes():
    """Test RetryConfig with custom retry status codes."""
    custom_statuses = (500, 502, 503)
    config = RetryConfig(retry_statuses=custom_statuses)
    
    assert config.retry_statuses == custom_statuses
    
    # Test with custom statuses
    mock_response = Mock()
    mock_response.status_code = 429
    exception = httpx.HTTPStatusError(
        message="Rate limit",
        request=Mock(),
        response=mock_response,
    )
    # 429 not in custom list, should not retry
    assert should_retry(exception, 0, config) is False
    
    # 500 is in custom list, should retry
    mock_response.status_code = 500
    assert should_retry(exception, 0, config) is True

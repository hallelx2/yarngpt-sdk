"""Retry configuration and utilities for YarnGPT SDK."""

from dataclasses import dataclass
from typing import Optional, Callable, Type, Tuple
import time
import random
from functools import wraps
import httpx

from .exceptions import YarnGPTError, QuotaExceededError, AuthenticationError


@dataclass
class RetryConfig:
    """
    Configuration for retry behavior.
    
    Attributes:
        max_retries: Maximum number of retry attempts (default: 3)
        backoff_factor: Multiplier for exponential backoff (default: 2.0)
        max_backoff: Maximum backoff time in seconds (default: 60)
        retry_statuses: HTTP status codes that should trigger a retry
        jitter: Add random jitter to backoff time (default: True)
    """
    max_retries: int = 3
    backoff_factor: float = 2.0
    max_backoff: float = 60.0
    retry_statuses: Tuple[int, ...] = (429, 500, 502, 503, 504)
    jitter: bool = True
    
    def __post_init__(self):
        """Validate configuration."""
        if self.max_retries < 0:
            raise ValueError("max_retries must be >= 0")
        if self.backoff_factor < 1:
            raise ValueError("backoff_factor must be >= 1")
        if self.max_backoff < 0:
            raise ValueError("max_backoff must be >= 0")


def calculate_backoff(attempt: int, config: RetryConfig) -> float:
    """
    Calculate backoff time for a given attempt.
    
    Args:
        attempt: Current retry attempt number (0-indexed)
        config: Retry configuration
        
    Returns:
        Backoff time in seconds
    """
    # Exponential backoff: base * (factor ^ attempt)
    backoff = min(config.backoff_factor ** attempt, config.max_backoff)
    
    # Add jitter to prevent thundering herd
    if config.jitter:
        backoff *= (0.5 + random.random())  # Random factor between 0.5 and 1.5
    
    return backoff


def should_retry(
    exception: Exception,
    attempt: int,
    config: RetryConfig,
) -> bool:
    """
    Determine if an exception should trigger a retry.
    
    Args:
        exception: The exception that was raised
        attempt: Current retry attempt number
        config: Retry configuration
        
    Returns:
        True if should retry, False otherwise
    """
    # Don't retry if we've exceeded max attempts
    if attempt >= config.max_retries:
        return False
    
    # Don't retry authentication errors
    if isinstance(exception, AuthenticationError):
        return False
    
    # Don't retry quota exceeded errors (daily limit)
    if isinstance(exception, QuotaExceededError):
        return False
    
    # Retry on network errors
    if isinstance(exception, (httpx.TimeoutException, httpx.NetworkError)):
        return True
    
    # Retry on specific HTTP status codes
    if isinstance(exception, httpx.HTTPStatusError):
        return exception.response.status_code in config.retry_statuses
    
    return False


def with_retry(config: Optional[RetryConfig] = None):
    """
    Decorator to add retry logic to a function.
    
    Args:
        config: Retry configuration (uses default if None)
        
    Example:
        @with_retry(RetryConfig(max_retries=5))
        def make_api_call():
            response = client.get("/api/endpoint")
            response.raise_for_status()
            return response
    """
    if config is None:
        config = RetryConfig()
    
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(config.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if not should_retry(e, attempt, config):
                        raise
                    
                    if attempt < config.max_retries:
                        backoff_time = calculate_backoff(attempt, config)
                        time.sleep(backoff_time)
            
            # If we get here, we've exhausted all retries
            raise last_exception
        
        return wrapper
    return decorator


def with_retry_async(config: Optional[RetryConfig] = None):
    """
    Async decorator to add retry logic to an async function.
    
    Args:
        config: Retry configuration (uses default if None)
        
    Example:
        @with_retry_async(RetryConfig(max_retries=5))
        async def make_api_call():
            response = await client.get("/api/endpoint")
            response.raise_for_status()
            return response
    """
    import asyncio
    
    if config is None:
        config = RetryConfig()
    
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(config.max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if not should_retry(e, attempt, config):
                        raise
                    
                    if attempt < config.max_retries:
                        backoff_time = calculate_backoff(attempt, config)
                        await asyncio.sleep(backoff_time)
            
            # If we get here, we've exhausted all retries
            raise last_exception
        
        return wrapper
    return decorator

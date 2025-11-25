"""Test script to verify quota/rate limit error handling."""

from yarngpt import YarnGPT
from yarngpt.exceptions import APIError, AuthenticationError, QuotaExceededError


def test_quota_handling():
    """Test that quota errors are properly handled"""
    print("=" * 60)
    print("Testing Quota/Rate Limit Error Handling")
    print("=" * 60)
    print("\nYarnGPT Free Tier Limits:")
    print("  - TTS Requests: 80/day")
    print("  - Media Processing: 8/day")
    print("  - URL Extractions: 100/day")
    print("  - Chunked Audio: 120/day")
    print("=" * 60)

    try:
        with YarnGPT() as client:
            # Make multiple requests to potentially hit quota
            for i in range(10):
                print(f"\nRequest {i + 1}/10...")
                try:
                    audio = client.text_to_speech(f"Test message number {i + 1}")
                    print(f"✓ Success - Generated {len(audio):,} bytes")
                except QuotaExceededError as e:
                    print(f"\n⚠️  Quota Exceeded: {e}")
                    print("\nThis is expected when you've reached your daily limit.")
                    print("Free tier allows 80 TTS requests per day.")
                    print("The SDK properly caught the QuotaExceededError!")
                    return
                except APIError as e:
                    print(f"\n✗ API Error: {e}")
                    return
                except AuthenticationError as e:
                    print(f"\n✗ Auth Error: {e}")
                    return

            print("\n✓ All requests completed successfully!")

    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")


if __name__ == "__main__":
    test_quota_handling()

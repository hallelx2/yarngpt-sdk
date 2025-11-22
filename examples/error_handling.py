"""Example: Error handling."""

from yarngpt import YarnGPT, Voice
from yarngpt.exceptions import (
    AuthenticationError,
    ValidationError,
    APIError,
    YarnGPTError
)
import os

def main():
    api_key = os.getenv("YARNGPT_API_KEY", "your_api_key_here")
    
    print("Demonstrating error handling...\n")
    
    # Example 1: Invalid API key
    print("1. Testing authentication error...")
    try:
        client = YarnGPT(api_key="invalid_key")
        client.text_to_speech("This will fail")
    except AuthenticationError as e:
        print(f"   ✓ Caught authentication error: {e}\n")
    
    # Example 2: Empty text
    print("2. Testing validation error (empty text)...")
    try:
        client = YarnGPT(api_key=api_key)
        client.text_to_speech("")
    except ValidationError as e:
        print(f"   ✓ Caught validation error: {e}\n")
    
    # Example 3: Text too long
    print("3. Testing validation error (text too long)...")
    try:
        client = YarnGPT(api_key=api_key)
        long_text = "A" * 2001  # Exceeds 2000 character limit
        client.text_to_speech(long_text)
    except ValidationError as e:
        print(f"   ✓ Caught validation error: {e}\n")
    
    # Example 4: Successful request with error handling
    print("4. Making successful request with error handling...")
    try:
        client = YarnGPT(api_key=api_key)
        audio = client.text_to_speech(
            text="This request should succeed!",
            voice=Voice.IDERA
        )
        with open("error_handling_success.mp3", "wb") as f:
            f.write(audio)
        print("   ✓ Success! Saved to error_handling_success.mp3\n")
    except YarnGPTError as e:
        print(f"   ✗ Error: {e}\n")
    finally:
        client.close()
    
    print("✓ Error handling examples completed")

if __name__ == "__main__":
    main()

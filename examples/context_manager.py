"""Example: Using context manager for proper resource management."""

from yarngpt import YarnGPT, Voice
import os


def main():
    api_key = os.getenv("YARNGPT_API_KEY", "your_api_key_here")

    # Using context manager ensures proper cleanup
    with YarnGPT(api_key=api_key) as client:
        print("Generating speech with context manager...")

        audio = client.text_to_speech(
            text="Using context manager ensures proper resource cleanup.", voice=Voice.IDERA
        )

        with open("context_manager_output.mp3", "wb") as f:
            f.write(audio)

        print("✓ Saved to context_manager_output.mp3")

    # Client is automatically closed here
    print("✓ Client closed automatically")


if __name__ == "__main__":
    main()

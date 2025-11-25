"""
Quick test script for YarnGPT SDK
Tests basic functionality with minimal API calls
"""

from yarngpt import YarnGPT, Voice
from yarngpt.exceptions import YarnGPTError


def test_basic_tts():
    """Test basic text-to-speech with one voice"""
    print("=" * 50)
    print("YarnGPT SDK - Quick Test")
    print("=" * 50)

    try:
        # Test 1: Basic request with default settings (auto-loads from .env)
        print("\n[Test 1/5] Basic TTS with default voice...")
        with YarnGPT() as client:
            audio = client.text_to_speech("Hello from YarnGPT SDK!")

            with open("test_basic.mp3", "wb") as f:
                f.write(audio)

            print(f"✓ Success! Generated {len(audio):,} bytes")
            print("  Saved to: test_basic.mp3")

        # Test 2: Specific voice
        print("\n[Test 2/5] TTS with Emma voice...")
        with YarnGPT() as client:
            audio = client.text_to_speech(
                text="Testing Emma's authoritative voice.", voice=Voice.EMMA
            )

            with open("test_emma.mp3", "wb") as f:
                f.write(audio)

            print(f"✓ Success! Generated {len(audio):,} bytes")
            print("  Saved to: test_emma.mp3")

        # Test 3: Using convenience method
        print("\n[Test 3/5] Using text_to_speech_file method...")
        with YarnGPT() as client:
            output_path = client.text_to_speech_file(
                text="This is a test using the convenience method.",
                output_path="test_convenience.mp3",
                voice=Voice.JUDE,
            )
            print(f"✓ Success! Saved to: {output_path}")

        # Test 4: Batch processing with list
        print("\n[Test 4/5] Batch processing (2 texts)...")
        with YarnGPT() as client:
            texts = ["First batch text.", "Second batch text."]
            paths = client.batch_text_to_speech_files(
                texts, output_dir="batch_output", filename_prefix="batch", voice=Voice.TAYO
            )
            print(f"✓ Success! Generated {len(paths)} files")
            for path in paths:
                print(f"  - {path}")

        # Summary
        print("\n" + "=" * 50)
        print("✓ All tests passed! (5/8 requests used)")
        print("=" * 50)
        print("\nGenerated files:")
        print("  - test_basic.mp3")
        print("  - test_emma.mp3")
        print("  - test_convenience.mp3")
        print("  - batch_output/batch_0.mp3")
        print("  - batch_output/batch_1.mp3")

    except YarnGPTError as e:
        print(f"\n✗ Error: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False

    return True


if __name__ == "__main__":
    success = test_basic_tts()
    exit(0 if success else 1)

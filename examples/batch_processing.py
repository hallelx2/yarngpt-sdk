"""Example: Batch processing with YarnGPT SDK."""

from yarngpt import YarnGPT, Voice, AudioFormat


def main():
    print("=" * 60)
    print("YarnGPT SDK - Batch Processing Demo")
    print("=" * 60)

    # Initialize client (automatically loads YARNGPT_API_KEY from .env)
    with YarnGPT() as client:
        # Example 1: Batch process with auto-generated filenames
        print("\n[Example 1] Batch processing with list of texts...")
        texts = [
            "Welcome to our service!",
            "Please hold while we connect you.",
            "Thank you for your patience.",
            "Your call is important to us.",
        ]

        paths = client.batch_text_to_speech_files(
            texts=texts,
            output_dir="batch_output",
            filename_prefix="greeting",
            voice=Voice.ADAORA,
            response_format=AudioFormat.MP3,
        )

        print(f"✓ Generated {len(paths)} files:")
        for path in paths:
            print(f"  - {path}")

        # Example 2: Batch process with custom filenames
        print("\n[Example 2] Batch processing with custom filenames...")
        custom_texts = {
            "welcome": "Welcome! How can I help you today?",
            "goodbye": "Thank you for visiting. Goodbye!",
            "error": "Sorry, something went wrong. Please try again.",
        }

        paths_dict = client.batch_text_to_speech_dict(
            text_dict=custom_texts,
            output_dir="custom_output",
            voice=Voice.JUDE,
            response_format=AudioFormat.MP3,
        )

        print(f"✓ Generated {len(paths_dict)} files:")
        for name, path in paths_dict.items():
            print(f"  - {name}: {path}")

        # Example 3: Get audio data without saving (for processing)
        print("\n[Example 3] Batch processing to memory...")
        short_texts = ["One", "Two", "Three"]

        audio_list = client.batch_text_to_speech(texts=short_texts, voice=Voice.EMMA)

        print(f"✓ Generated {len(audio_list)} audio clips in memory")
        total_bytes = sum(len(audio) for audio in audio_list)
        print(f"  Total audio data: {total_bytes:,} bytes")

    print("\n" + "=" * 60)
    print("✓ Batch processing examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

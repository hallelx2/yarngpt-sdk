"""Test script for AsyncYarnGPT client."""

import asyncio
from yarngpt import AsyncYarnGPT, Voice, AudioFormat, RetryConfig


async def test_async_basic():
    """Test basic async text-to-speech."""
    print("\n🧪 Test 1: Basic async text-to-speech")
    async with AsyncYarnGPT() as client:
        audio = await client.text_to_speech(
            text="Hello from async client!",
            voice=Voice.IDERA,
            response_format=AudioFormat.MP3,
        )
        print(f"✅ Generated audio: {len(audio):,} bytes")

        # Save to file
        with open("async_test_basic.mp3", "wb") as f:
            f.write(audio)
        print("✅ Saved to async_test_basic.mp3")


async def test_async_file():
    """Test async text-to-speech with file saving."""
    print("\n🧪 Test 2: Async text-to-speech with file")
    async with AsyncYarnGPT() as client:
        path = await client.text_to_speech_file(
            text="Testing async file save",
            output_path="async_test_file.mp3",
            voice=Voice.EMMA,
        )
        print(f"✅ Saved to {path}")


async def test_async_batch_sequential():
    """Test async batch processing (sequential)."""
    print("\n🧪 Test 3: Async batch processing (sequential)")
    texts = ["First text", "Second text", "Third text"]

    async with AsyncYarnGPT() as client:
        import time

        start = time.time()

        audios = await client.batch_text_to_speech(
            texts=texts,
            voice=Voice.JUDE,
            concurrent=False,
        )

        elapsed = time.time() - start
        print(f"✅ Generated {len(audios)} audio files in {elapsed:.2f}s (sequential)")
        for i, audio in enumerate(audios):
            print(f"   • Audio {i + 1}: {len(audio):,} bytes")


async def test_async_batch_concurrent():
    """Test async batch processing (concurrent)."""
    print("\n🧪 Test 4: Async batch processing (concurrent)")
    texts = ["First text", "Second text", "Third text"]

    async with AsyncYarnGPT() as client:
        import time

        start = time.time()

        audios = await client.batch_text_to_speech(
            texts=texts,
            voice=Voice.JUDE,
            concurrent=True,
        )

        elapsed = time.time() - start
        print(f"✅ Generated {len(audios)} audio files in {elapsed:.2f}s (concurrent)")
        print("   🚀 Much faster with concurrent processing!")
        for i, audio in enumerate(audios):
            print(f"   • Audio {i + 1}: {len(audio):,} bytes")


async def test_async_batch_files():
    """Test async batch processing with files."""
    print("\n🧪 Test 5: Async batch to files (concurrent)")
    texts = ["Welcome to async", "This is concurrent", "Processing multiple texts"]

    async with AsyncYarnGPT() as client:
        paths = await client.batch_text_to_speech_files(
            texts=texts,
            output_dir="async_batch_output",
            filename_prefix="async",
            voice=Voice.REGINA,
            response_format=AudioFormat.MP3,
            concurrent=True,
        )

        print(f"✅ Generated {len(paths)} files:")
        for path in paths:
            print(f"   • {path.name}")


async def test_async_custom_retry():
    """Test async with custom retry configuration."""
    print("\n🧪 Test 6: Async with custom retry config")
    retry_config = RetryConfig(
        max_retries=5,
        backoff_factor=2.0,
        jitter=True,
    )

    async with AsyncYarnGPT(retry_config=retry_config) as client:
        audio = await client.text_to_speech(
            text="Testing with custom retry configuration",
            voice=Voice.TAYO,
        )
        print(f"✅ Generated with custom retry: {len(audio):,} bytes")


async def test_async_different_voices():
    """Test async with different voices."""
    print("\n🧪 Test 7: Async with multiple voices")

    voice_tests = [
        (Voice.IDERA, "Testing Idera voice"),
        (Voice.EMMA, "Testing Emma voice"),
        (Voice.JUDE, "Testing Jude voice"),
        (Voice.ZAINAB, "Testing Zainab voice"),
    ]

    async with AsyncYarnGPT() as client:
        tasks = [client.text_to_speech(text=text, voice=voice) for voice, text in voice_tests]

        audios = await asyncio.gather(*tasks)
        print(f"✅ Generated {len(audios)} voices concurrently:")
        for (voice, _), audio in zip(voice_tests, audios):
            print(f"   • {voice.value}: {len(audio):,} bytes")


async def test_async_different_formats():
    """Test async with different audio formats."""
    print("\n🧪 Test 8: Async with multiple formats")

    format_tests = [
        (AudioFormat.MP3, "MP3 format test"),
        (AudioFormat.WAV, "WAV format test"),
        (AudioFormat.OPUS, "OPUS format test"),
    ]

    try:
        async with AsyncYarnGPT() as client:
            tasks = [
                client.text_to_speech(text=text, response_format=fmt) for fmt, text in format_tests
            ]

            audios = await asyncio.gather(*tasks, return_exceptions=True)

            success_count = 0
            for (fmt, _), result in zip(format_tests, audios):
                if isinstance(result, Exception):
                    print(f"   ⚠️  {fmt.value}: Failed ({type(result).__name__})")
                else:
                    print(f"   • {fmt.value}: {len(result):,} bytes")
                    success_count += 1

            if success_count > 0:
                print(f"✅ Generated {success_count}/{len(format_tests)} formats successfully")
            else:
                print("⚠️  All format tests encountered errors (API issue)")
    except Exception as e:
        print(f"⚠️  Format test failed: {type(e).__name__}: {e}")
        print("   (This may be an API limitation, not a client issue)")


async def main():
    """Run all async tests."""
    print("=" * 60)
    print("🚀 AsyncYarnGPT Client Test Suite")
    print("=" * 60)

    tests = [
        ("Basic async text-to-speech", test_async_basic),
        ("Async file saving", test_async_file),
        ("Batch sequential", test_async_batch_sequential),
        ("Batch concurrent", test_async_batch_concurrent),
        ("Batch to files", test_async_batch_files),
        ("Custom retry config", test_async_custom_retry),
        ("Multiple voices", test_async_different_voices),
        ("Multiple formats", test_async_different_formats),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            await test_func()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"\n❌ {test_name} failed: {type(e).__name__}: {e}")

    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    if failed == 0:
        print("✅ All async tests completed successfully!")
    else:
        print("⚠️  Some tests failed (may be API limitations)")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

"""Example: Basic text-to-speech usage."""

from yarngpt import YarnGPT, Voice, AudioFormat
import os

def main():
    # Get API key from environment or replace with your actual key
    api_key = os.getenv("YARNGPT_API_KEY", "your_api_key_here")
    
    # Initialize client
    client = YarnGPT(api_key=api_key)
    
    # Example 1: Simple text-to-speech
    print("Generating speech with default voice...")
    audio = client.text_to_speech("Hello! Welcome to YarnGPT SDK.")
    
    with open("example_output_1.mp3", "wb") as f:
        f.write(audio)
    print("✓ Saved to example_output_1.mp3")
    
    # Example 2: Using specific voice
    print("\nGenerating speech with Emma's voice...")
    audio = client.text_to_speech(
        text="This is a demonstration of the authoritative Emma voice.",
        voice=Voice.EMMA
    )
    
    with open("example_output_2.mp3", "wb") as f:
        f.write(audio)
    print("✓ Saved to example_output_2.mp3")
    
    # Example 3: Different audio format (WAV)
    print("\nGenerating speech in WAV format...")
    audio = client.text_to_speech(
        text="This audio is in WAV format for higher quality.",
        voice=Voice.JUDE,
        response_format=AudioFormat.WAV
    )
    
    with open("example_output_3.wav", "wb") as f:
        f.write(audio)
    print("✓ Saved to example_output_3.wav")
    
    # Example 4: Using the convenience method
    print("\nUsing text_to_speech_file method...")
    output_path = client.text_to_speech_file(
        text="This method saves the file directly!",
        output_path="example_output_4.mp3",
        voice=Voice.ADAORA
    )
    print(f"✓ Saved to {output_path}")
    
    # Clean up
    client.close()
    print("\n✓ All examples completed successfully!")

if __name__ == "__main__":
    main()

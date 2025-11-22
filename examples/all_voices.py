"""Example: Generate speech with all available voices."""

from yarngpt import YarnGPT, Voice
import os

def main():
    api_key = os.getenv("YARNGPT_API_KEY", "your_api_key_here")
    
    text = "Hello! This is a sample of my voice."
    
    with YarnGPT(api_key=api_key) as client:
        print("Generating samples for all voices...\n")
        
        for voice in Voice:
            print(f"Generating: {voice.value} ({voice.description})")
            
            try:
                output_path = client.text_to_speech_file(
                    text=text,
                    output_path=f"voices/voice_{voice.value.lower()}.mp3",
                    voice=voice
                )
                print(f"  ✓ Saved to {output_path}\n")
            except Exception as e:
                print(f"  ✗ Error: {e}\n")
        
        print("✓ All voice samples generated!")

if __name__ == "__main__":
    main()

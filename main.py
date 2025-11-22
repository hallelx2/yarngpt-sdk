"""
YarnGPT SDK Demo Script

This is a simple demo of the YarnGPT SDK.
For more examples, see the examples/ directory.
"""

from yarngpt import YarnGPT, Voice
import os

def main():
    print("YarnGPT SDK - Quick Demo")
    print("=" * 40)
    
    # Get API key from environment
    api_key = os.getenv("YARNGPT_API_KEY")
    
    if not api_key:
        print("\n⚠️  Please set your YARNGPT_API_KEY environment variable")
        print("   Get your API key from: https://yarngpt.ai/account")
        print("\n   Windows (PowerShell): $env:YARNGPT_API_KEY='your_key'")
        print("   Windows (CMD):        set YARNGPT_API_KEY=your_key")
        print("   Linux/Mac:           export YARNGPT_API_KEY='your_key'")
        return
    
    # Create client and generate speech
    try:
        with YarnGPT(api_key=api_key) as client:
            print(f"\n✓ Connected to YarnGPT API")
            print(f"  Generating speech with {Voice.IDERA.value} voice...")
            
            audio = client.text_to_speech(
                text="Hello! Welcome to YarnGPT SDK. This is a text-to-speech API for Nigerian accents.",
                voice=Voice.IDERA
            )
            
            output_file = "demo_output.mp3"
            with open(output_file, "wb") as f:
                f.write(audio)
            
            print(f"\n✓ Speech generated successfully!")
            print(f"  Saved to: {output_file}")
            print(f"  Audio size: {len(audio):,} bytes")
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return
    
    print("\n" + "=" * 40)
    print("For more examples, check the examples/ directory")
    print("Documentation: https://github.com/yarngpt/yarngpt-sdk")


if __name__ == "__main__":
    main()


"""Data models and enums for YarnGPT SDK."""

from enum import Enum


class Voice(str, Enum):
    """Available voice characters for text-to-speech conversion."""
    
    IDERA = "Idera"  # Melodic, gentle
    EMMA = "Emma"  # Authoritative, deep
    ZAINAB = "Zainab"  # Soothing, gentle
    OSAGIE = "Osagie"  # Smooth, calm
    WURA = "Wura"  # Young, sweet
    JUDE = "Jude"  # Warm, confident
    CHINENYE = "Chinenye"  # Engaging, warm
    TAYO = "Tayo"  # Upbeat, energetic
    REGINA = "Regina"  # Mature, warm
    FEMI = "Femi"  # Rich, reassuring
    ADAORA = "Adaora"  # Warm, engaging
    UMAR = "Umar"  # Calm, smooth
    MARY = "Mary"  # Energetic, youthful
    NONSO = "Nonso"  # Bold, resonant
    REMI = "Remi"  # Melodious, warm
    ADAM = "Adam"  # Deep, clear
    
    @property
    def description(self) -> str:
        """Get the voice description."""
        descriptions = {
            Voice.IDERA: "Melodic, gentle",
            Voice.EMMA: "Authoritative, deep",
            Voice.ZAINAB: "Soothing, gentle",
            Voice.OSAGIE: "Smooth, calm",
            Voice.WURA: "Young, sweet",
            Voice.JUDE: "Warm, confident",
            Voice.CHINENYE: "Engaging, warm",
            Voice.TAYO: "Upbeat, energetic",
            Voice.REGINA: "Mature, warm",
            Voice.FEMI: "Rich, reassuring",
            Voice.ADAORA: "Warm, engaging",
            Voice.UMAR: "Calm, smooth",
            Voice.MARY: "Energetic, youthful",
            Voice.NONSO: "Bold, resonant",
            Voice.REMI: "Melodious, warm",
            Voice.ADAM: "Deep, clear",
        }
        return descriptions.get(self, "")


class AudioFormat(str, Enum):
    """Supported audio output formats."""
    
    MP3 = "mp3"
    WAV = "wav"
    OPUS = "opus"
    FLAC = "flac"

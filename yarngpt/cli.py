"""Command-line interface for YarnGPT SDK."""

import sys
from pathlib import Path
from typing import Optional, List
import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import print as rprint

from yarngpt import YarnGPT, Voice, AudioFormat
from yarngpt.exceptions import (
    YarnGPTError,
    AuthenticationError,
    ValidationError,
    QuotaExceededError,
)

# Nigerian flag colors: Green - White - Green
BANNER = """
██╗   ██╗ █████╗ ██████╗ ███╗   ██╗ ██████╗ ██████╗ ████████╗
╚██╗ ██╔╝██╔══██╗██╔══██╗████╗  ██║██╔════╝ ██╔══██╗╚══██╔══╝
 ╚████╔╝ ███████║██████╔╝██╔██╗ ██║██║  ███╗██████╔╝   ██║   
  ╚██╔╝  ██╔══██║██╔══██╗██║╚██╗██║██║   ██║██╔═══╝    ██║   
   ██║   ██║  ██║██║  ██║██║ ╚████║╚██████╔╝██║        ██║   
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝        ╚═╝   
"""

TAGLINE = "Nigerian Accent Text-to-Speech - Authentic Voices, Powered by AI"

from typer.core import TyperGroup


class BannerGroup(TyperGroup):
    """Custom Typer group that shows banner before help output."""
    
    def format_help(self, ctx, formatter):
        # Show banner before help
        show_banner()
        super().format_help(ctx, formatter)


app = typer.Typer(
    name="yarngpt",
    help="YarnGPT Text-to-Speech CLI - Convert text to speech with Nigerian accents",
    add_completion=False,
    no_args_is_help=False,
    cls=BannerGroup,
)
console = Console()


def show_banner():
    """Display the styled ASCII art banner with Nigerian flag colors (Green-White-Green)."""
    banner_lines = BANNER.strip().split("\n")
    
    # Nigerian flag gradient: Green -> White -> Green
    # Using rich color names that blend smoothly
    colors = [
        "green",           # Top - Green
        "bright_green",    # 
        "white",           # Middle - White
        "bright_green",    # 
        "green",           # Bottom - Green
    ]
    
    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=f"bold {color}")
    
    console.print(Align.center(styled_banner))
    console.print(Align.center(Text(TAGLINE, style="italic bright_yellow")))
    console.print()


def get_client(api_key: Optional[str] = None) -> YarnGPT:
    """Create and return a YarnGPT client instance."""
    try:
        return YarnGPT(api_key=api_key)
    except AuthenticationError as e:
        console.print(f"[red]Authentication Error:[/red] {e}", style="bold")
        console.print("\n💡 Get your API key from: https://yarngpt.ai/account")
        raise typer.Exit(1)


@app.command()
def convert(
    text: str = typer.Argument(..., help="Text to convert to speech"),
    output: Path = typer.Option(
        "output.mp3",
        "--output",
        "-o",
        help="Output file path",
    ),
    voice: str = typer.Option(
        "idera",
        "--voice",
        "-v",
        help="Voice name (e.g., idera, emma, jude)",
    ),
    format: str = typer.Option(
        "mp3",
        "--format",
        "-f",
        help="Audio format (mp3, wav, opus, flac)",
    ),
    api_key: Optional[str] = typer.Option(
        None,
        "--api-key",
        "-k",
        help="YarnGPT API key (or set YARNGPT_API_KEY env var)",
        envvar="YARNGPT_API_KEY",
    ),
):
    """
    Convert text to speech and save to a file.

    Examples:

        yarngpt convert "Hello, welcome to Nigeria!"

        yarngpt convert "Good morning" -o greeting.mp3 -v emma

        yarngpt convert "Test audio" --voice jude --format wav
    """
    try:
        # Validate voice
        voice_upper = voice.upper()
        if not hasattr(Voice, voice_upper):
            console.print(f"[red]Invalid voice:[/red] {voice}", style="bold")
            console.print("\n💡 Use 'yarngpt voices' to see available voices")
            raise typer.Exit(1)

        # Validate format
        format_upper = format.upper()
        if not hasattr(AudioFormat, format_upper):
            console.print(f"[red]Invalid format:[/red] {format}", style="bold")
            console.print("\n💡 Supported formats: mp3, wav, opus, flac")
            raise typer.Exit(1)

        voice_enum = getattr(Voice, voice_upper)
        format_enum = getattr(AudioFormat, format_upper)

        client = get_client(api_key)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(description="🎤 Generating speech...", total=None)

            audio = client.text_to_speech(
                text=text,
                voice=voice_enum,
                response_format=format_enum,
            )

        # Save to file
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "wb") as f:
            f.write(audio)

        console.print(
            f"\n✅ [green]Success![/green] Audio saved to: [cyan]{output}[/cyan]"
        )
        console.print(f"   Size: {len(audio):,} bytes")
        console.print(f"   Voice: {voice_enum.value}")
        console.print(f"   Format: {format_enum.value}")

    except ValidationError as e:
        console.print(f"[red]Validation Error:[/red] {e}", style="bold")
        raise typer.Exit(1)
    except QuotaExceededError as e:
        console.print(f"[red]Quota Exceeded:[/red] {e}", style="bold")
        console.print("\n💡 Free tier: 80 TTS requests/day")
        console.print("   Upgrade at: https://yarngpt.ai/account")
        raise typer.Exit(1)
    except YarnGPTError as e:
        console.print(f"[red]Error:[/red] {e}", style="bold")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected Error:[/red] {e}", style="bold")
        raise typer.Exit(1)


@app.command()
def batch(
    input_file: Path = typer.Argument(
        ...,
        help="Text file with one line per audio (or JSON file with text array)",
    ),
    output_dir: Path = typer.Option(
        "output",
        "--output-dir",
        "-o",
        help="Output directory for audio files",
    ),
    voice: str = typer.Option(
        "idera",
        "--voice",
        "-v",
        help="Voice name for all files",
    ),
    format: str = typer.Option(
        "mp3",
        "--format",
        "-f",
        help="Audio format for all files",
    ),
    prefix: str = typer.Option(
        "audio",
        "--prefix",
        "-p",
        help="Filename prefix for generated files",
    ),
    api_key: Optional[str] = typer.Option(
        None,
        "--api-key",
        "-k",
        help="YarnGPT API key",
        envvar="YARNGPT_API_KEY",
    ),
):
    """
    Batch convert multiple texts to speech from a file.

    Input file should be a text file with one text per line, or a JSON file
    with an array of strings.

    Examples:

        yarngpt batch texts.txt

        yarngpt batch texts.txt -o audio_files -v emma --prefix speech
    """
    import json

    if not input_file.exists():
        console.print(f"[red]Error:[/red] File not found: {input_file}", style="bold")
        raise typer.Exit(1)

    try:
        # Read input file
        if input_file.suffix == ".json":
            with open(input_file, "r", encoding="utf-8") as f:
                texts = json.load(f)
        else:
            with open(input_file, "r", encoding="utf-8") as f:
                texts = [line.strip() for line in f if line.strip()]

        if not texts:
            console.print("[red]Error:[/red] No texts found in file", style="bold")
            raise typer.Exit(1)

        # Validate voice and format
        voice_upper = voice.upper()
        format_upper = format.upper()

        if not hasattr(Voice, voice_upper):
            console.print(f"[red]Invalid voice:[/red] {voice}", style="bold")
            raise typer.Exit(1)
        if not hasattr(AudioFormat, format_upper):
            console.print(f"[red]Invalid format:[/red] {format}", style="bold")
            raise typer.Exit(1)

        voice_enum = getattr(Voice, voice_upper)
        format_enum = getattr(AudioFormat, format_upper)

        client = get_client(api_key)

        console.print(f"\n📝 Processing {len(texts)} texts...")
        console.print(f"   Voice: {voice_enum.value}")
        console.print(f"   Format: {format_enum.value}")
        console.print(f"   Output: {output_dir}/\n")

        # Process batch
        with Progress(console=console) as progress:
            task = progress.add_task(
                "[cyan]Converting...", total=len(texts)
            )

            paths = client.batch_text_to_speech_files(
                texts=texts,
                output_dir=output_dir,
                filename_prefix=prefix,
                voice=voice_enum,
                response_format=format_enum,
            )

            for _ in paths:
                progress.advance(task)

        console.print(f"\n✅ [green]Success![/green] Generated {len(paths)} audio files")
        console.print(f"   Location: [cyan]{output_dir}/[/cyan]")

        # Show first few files
        for i, path in enumerate(paths[:5]):
            console.print(f"   • {path.name}")
        if len(paths) > 5:
            console.print(f"   ... and {len(paths) - 5} more")

    except YarnGPTError as e:
        console.print(f"[red]Error:[/red] {e}", style="bold")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected Error:[/red] {e}", style="bold")
        raise typer.Exit(1)


@app.command()
def voices():
    """List all available voices with descriptions."""
    table = Table(title="🎤 Available YarnGPT Voices", show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan", width=12)
    table.add_column("Value", style="green", width=12)
    table.add_column("Description", style="white")

    # Voice descriptions
    voice_info = {
        Voice.IDERA: "Melodic and gentle voice",
        Voice.EMMA: "Authoritative and deep voice",
        Voice.ZAINAB: "Soothing and gentle voice",
        Voice.OSAGIE: "Smooth and calm voice",
        Voice.WURA: "Young and sweet voice",
        Voice.JUDE: "Warm and confident voice",
        Voice.CHINENYE: "Engaging and warm voice",
        Voice.TAYO: "Upbeat and energetic voice",
        Voice.REGINA: "Mature and warm voice",
        Voice.FEMI: "Rich and reassuring voice",
        Voice.ADAORA: "Warm and engaging voice",
        Voice.UMAR: "Calm and smooth voice",
        Voice.MARY: "Energetic and youthful voice",
        Voice.NONSO: "Bold and resonant voice",
        Voice.REMI: "Melodious and warm voice",
        Voice.ADAM: "Deep and clear voice",
    }

    for voice_enum in Voice:
        table.add_row(
            voice_enum.name,
            voice_enum.value,
            voice_info.get(voice_enum, ""),
        )

    console.print(table)
    console.print("\n💡 Usage: [cyan]yarngpt convert \"Hello\" --voice idera[/cyan]")


@app.command()
def formats():
    """List all supported audio formats."""
    table = Table(title="🔊 Supported Audio Formats", show_header=True, header_style="bold magenta")
    table.add_column("Format", style="cyan", width=12)
    table.add_column("Extension", style="green", width=12)
    table.add_column("Description", style="white")

    formats_info = [
        (AudioFormat.MP3, "mp3", "MPEG Audio Layer III - Compressed, widely supported"),
        (AudioFormat.WAV, "wav", "Waveform Audio File Format - Uncompressed, high quality"),
        (AudioFormat.OPUS, "opus", "Opus codec - Low latency, good for streaming"),
        (AudioFormat.FLAC, "flac", "Free Lossless Audio Codec - Compressed, lossless"),
    ]

    for fmt, ext, desc in formats_info:
        table.add_row(fmt.value, ext, desc)

    console.print(table)
    console.print("\n💡 Usage: [cyan]yarngpt convert \"Hello\" --format wav[/cyan]")


@app.command()
def version():
    """Show the SDK version."""
    from yarngpt import __version__
    console.print(f"YarnGPT SDK version: [cyan]{__version__}[/cyan]")


@app.callback(invoke_without_command=True)
def main_callback(ctx: typer.Context):
    """Main callback to show banner when no command is provided."""
    if ctx.invoked_subcommand is None:
        show_banner()
        
        # Create welcome panel
        welcome_text = Text()
        welcome_text.append("Welcome to ", style="white")
        welcome_text.append("YarnGPT CLI", style="bold green")
        welcome_text.append("\nAuthentic Nigerian Accent Text-to-Speech", style="italic dim")
        
        welcome_panel = Panel(
            welcome_text,
            title="[bold green]🎤 YarnGPT[/bold green]",
            border_style="green",
            padding=(1, 2),
        )
        console.print(welcome_panel)
        console.print()
        
        # Command table
        table = Table(
            title="[bold green]Available Commands[/bold green]",
            show_header=True,
            header_style="bold bright_green",
        )
        table.add_column("Command", style="green", no_wrap=True)
        table.add_column("Description", style="white")
        table.add_column("Example", style="dim")
        
        table.add_row("convert", "Convert text to speech", 'yarngpt convert "Hello Nigeria!"')
        table.add_row("batch", "Batch convert from file", "yarngpt batch texts.txt")
        table.add_row("voices", "List available voices", "yarngpt voices")
        table.add_row("formats", "List audio formats", "yarngpt formats")
        table.add_row("info", "Show API limits", "yarngpt info")
        table.add_row("version", "Show SDK version", "yarngpt version")
        
        console.print(table)
        console.print()
        
        # Quick tips
        tips_panel = Panel(
            "[bold yellow]Quick Tips:[/bold yellow]\n"
            "• [bold green]🔑 Setup:[/bold green] export YARNGPT_API_KEY=your_key\n"
            "• [bold green]🎙️ Try Voices:[/bold green] yarngpt voices\n"
            "• [bold green]📝 Convert:[/bold green] yarngpt convert \"Your text\" -o output.mp3\n"
            "• [bold green]📚 Batch:[/bold green] yarngpt batch texts.txt --voice emma\n"
            "• [bold green]❓ Help:[/bold green] yarngpt --help or yarngpt <command> --help",
            title="[bold yellow]💡 Getting Started[/bold yellow]",
            border_style="yellow",
        )
        console.print(tips_panel)
        raise typer.Exit()


@app.command()
def info():
    """Show API information and limits."""
    console.print("\n[bold green]YarnGPT API Information[/bold green]\n")

    console.print("📊 [bold]Free Tier Limits:[/bold]")
    console.print("   • TTS Requests: 80/day")
    console.print("   • Max Text Length: 2,000 characters")
    console.print("   • Media Processing Jobs: 8/day")
    console.print("   • URL Extractions: 100/day")
    console.print("   • Chunked Audio Generations: 120/day\n")

    console.print("🎤 [bold]Features:[/bold]")
    console.print("   • 16 unique Nigerian voices")
    console.print("   • 4 audio formats (MP3, WAV, OPUS, FLAC)")
    console.print("   • Authentic Nigerian accents\n")

    console.print("🔗 [bold]Links:[/bold]")
    console.print("   • Website: https://yarngpt.ai")
    console.print("   • Account: https://yarngpt.ai/account")
    console.print("   • GitHub: https://github.com/hallelx2/yarngpt-sdk")
    console.print("   • PyPI: https://pypi.org/project/yarngpt-sdk/\n")

    console.print("💡 [bold]Get Started:[/bold]")
    console.print("   1. Get API key: https://yarngpt.ai/account")
    console.print("   2. Set environment variable: YARNGPT_API_KEY=your_key")
    console.print("   3. Run: yarngpt convert \"Hello, Nigeria!\"")


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()

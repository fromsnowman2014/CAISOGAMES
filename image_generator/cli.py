"""Command-line interface for image generator."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

try:
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
except ImportError:
    print("CLI dependencies not installed. Run: pip install click rich")
    sys.exit(1)

from .config import Config, load_config
from .generators.gemini_generator import GeminiGenerator
from .processors.sprite_processor import SpriteProcessor
from .processors.format_converter import FormatConverter
from .utils.cache import ImageCache
from .utils.logger import setup_logging, get_logger

console = Console()
logger = get_logger("cli")


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, verbose):
    """CAISOGAMES Image Generator - AI-powered game asset generation."""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose

    import logging
    level = logging.DEBUG if verbose else logging.INFO
    setup_logging(level=level)


@cli.command()
@click.argument('prompt')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--width', '-w', default=512, help='Image width')
@click.option('--height', '-h', default=512, help='Image height')
@click.option('--format', '-f', 'fmt', default='png', type=click.Choice(['png', 'jpg', 'gif', 'webp']))
@click.option('--style', '-s', default='pixel_art',
              type=click.Choice(['pixel_art', 'cartoon', 'realistic', 'sketch']))
@click.pass_context
def generate(ctx, prompt, output, width, height, fmt, style):
    """Generate an image from a text prompt."""
    config = load_config()

    if not config.gemini_api_key:
        console.print("[red]Error: GEMINI_API_KEY not set in environment[/red]")
        console.print("Set it via environment variable or .env file")
        sys.exit(1)

    async def _generate():
        generator = GeminiGenerator(config)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Generating image...", total=None)

            try:
                images = await generator.generate(
                    prompt=prompt,
                    width=width,
                    height=height,
                    style=style
                )

                progress.update(task, description="Processing...")

                if images:
                    image = images[0]

                    # Determine output path
                    if output:
                        output_path = Path(output)
                    else:
                        output_path = Path(f"generated_{style}.{fmt}")

                    # Convert format if needed
                    if fmt != 'png':
                        from PIL import Image as PILImage
                        import io
                        pil_image = PILImage.open(io.BytesIO(image.data))
                        converted = FormatConverter.convert(pil_image, fmt)
                        output_path.write_bytes(converted)
                    else:
                        output_path.write_bytes(image.data)

                    progress.update(task, description="Done!")
                    console.print(f"[green]Image saved to: {output_path}[/green]")

            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                if ctx.obj['verbose']:
                    console.print_exception()
                sys.exit(1)

    asyncio.run(_generate())


@cli.command()
@click.argument('prompt')
@click.argument('name')
@click.option('--size', '-s', default='64x64', help='Sprite size (WxH)')
@click.option('--output-dir', '-o', type=click.Path(), default='./assets/sprites')
@click.option('--pixelate/--no-pixelate', default=True, help='Apply pixel art effect')
@click.option('--colors', '-c', default=16, help='Number of colors in palette')
@click.pass_context
def sprite(ctx, prompt, name, size, output_dir, pixelate, colors):
    """Generate a game sprite."""
    config = load_config()

    if not config.gemini_api_key:
        console.print("[red]Error: GEMINI_API_KEY not set[/red]")
        sys.exit(1)

    # Parse size
    try:
        w, h = map(int, size.lower().split('x'))
    except ValueError:
        console.print("[red]Invalid size format. Use WxH (e.g., 64x64)[/red]")
        sys.exit(1)

    async def _generate_sprite():
        generator = GeminiGenerator(config)
        processor = SpriteProcessor(output_dir)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Generating sprite...", total=None)

            try:
                # Generate at higher resolution for better quality
                images = await generator.generate(
                    prompt=f"pixel art game sprite: {prompt}",
                    width=512,
                    height=512,
                    style='pixel_art'
                )

                if images:
                    progress.update(task, description="Processing sprite...")

                    from PIL import Image as PILImage
                    import io
                    pil_image = PILImage.open(io.BytesIO(images[0].data))

                    output_path = processor.process_sprite(
                        pil_image,
                        name=name,
                        size=(w, h),
                        remove_bg=True,
                        pixelate=pixelate,
                        pixel_size=max(1, 512 // w),
                        reduce_colors=True,
                        num_colors=colors
                    )

                    progress.update(task, description="Done!")
                    console.print(f"[green]Sprite saved to: {output_path}[/green]")

            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                if ctx.obj['verbose']:
                    console.print_exception()
                sys.exit(1)

    asyncio.run(_generate_sprite())


@cli.command()
@click.argument('frames', nargs=-1, type=click.Path(exists=True))
@click.argument('output', type=click.Path())
@click.option('--duration', '-d', default=100, help='Frame duration in ms')
@click.option('--loop/--no-loop', default=True, help='Loop animation')
def animate(frames, output, duration, loop):
    """Create an animated GIF from frame images."""
    if not frames:
        console.print("[red]No frames provided[/red]")
        sys.exit(1)

    try:
        output_path = FormatConverter.create_gif_from_files(
            list(frames),
            output,
            duration=duration,
            loop=0 if loop else 1
        )
        console.print(f"[green]Animation saved to: {output_path}[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--quality', '-q', default=95, help='Quality for lossy formats')
def convert(input_file, output_file, quality):
    """Convert image to a different format."""
    try:
        output_path = FormatConverter.convert_file(
            input_file,
            output_file,
            quality=quality
        )
        console.print(f"[green]Converted: {output_path}[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.option('--cache-dir', type=click.Path(), help='Cache directory')
def cache_stats(cache_dir):
    """Show cache statistics."""
    config = load_config()
    cache_path = Path(cache_dir) if cache_dir else config.cache_dir

    cache = ImageCache(cache_path)
    stats = cache.get_stats()

    table = Table(title="Cache Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Entries", str(stats['entries']))
    table.add_row("Total Size", f"{stats['total_size_mb']:.2f} MB")
    table.add_row("Max Size", f"{stats['max_size_mb']:.2f} MB")
    table.add_row("Usage", f"{stats['usage_percent']:.1f}%")

    console.print(table)


@cli.command()
@click.option('--cache-dir', type=click.Path(), help='Cache directory')
@click.confirmation_option(prompt='Clear all cached images?')
def cache_clear(cache_dir):
    """Clear the image cache."""
    config = load_config()
    cache_path = Path(cache_dir) if cache_dir else config.cache_dir

    cache = ImageCache(cache_path)
    count = cache.clear()

    console.print(f"[green]Cleared {count} cached images[/green]")


@cli.command()
def check_config():
    """Check configuration and API connectivity."""
    config = load_config()

    table = Table(title="Configuration Check")
    table.add_column("Setting", style="cyan")
    table.add_column("Status", style="green")

    # Check API key
    if config.gemini_api_key:
        table.add_row("GEMINI_API_KEY", "[green]Set[/green]")
    else:
        table.add_row("GEMINI_API_KEY", "[red]Not set[/red]")

    # Check directories
    table.add_row("Cache Directory", str(config.cache_dir))
    table.add_row("Default Output", str(config.default_output_dir))

    console.print(table)

    if not config.gemini_api_key:
        console.print("\n[yellow]To set the API key:[/yellow]")
        console.print("  export GEMINI_API_KEY=your_key_here")
        console.print("  or create a .env file with GEMINI_API_KEY=your_key_here")


def main():
    """Entry point for CLI."""
    cli(obj={})


if __name__ == '__main__':
    main()

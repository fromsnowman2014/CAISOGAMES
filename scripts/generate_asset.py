#!/usr/bin/env python3
"""
Game Asset Generator CLI

Generate game assets (sprites, backgrounds) using AI image generation.
Works via Vercel proxy when direct API access is blocked.

Usage:
    # Generate a sprite
    python scripts/generate_asset.py sprite "cute pixel art monster" monster_idle

    # Generate a background
    python scripts/generate_asset.py background "fantasy forest scene" forest_day

    # Generate with custom size
    python scripts/generate_asset.py sprite "dragon character" dragon --size 128x128

Environment Variables:
    VERCEL_APP_URL: Your Vercel deployment URL (required for proxy mode)
    GEMINI_API_KEY: Direct API access (alternative to proxy)
    USE_MOCK_GENERATOR: Set to 'true' for placeholder images

Example:
    export VERCEL_APP_URL=https://caisogames.vercel.app
    python scripts/generate_asset.py sprite "pixel art slime monster, green, bouncy" slime_idle
"""

import sys
import os
import asyncio
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from image_generator import ImageGeneratorService


async def generate_asset(
    asset_type: str,
    prompt: str,
    name: str,
    size: tuple = (64, 64),
    style: str = 'pixel_art'
):
    """Generate an asset and save it to the appropriate folder."""

    service = ImageGeneratorService()

    print(f"Generator: {service.generator_type}")
    print(f"Generating {asset_type}: {prompt[:50]}...")

    if asset_type == 'sprite':
        # Generate sprite
        output_dir = Path('assets/sprites')
        output_dir.mkdir(parents=True, exist_ok=True)

        image = await service.generate(
            prompt=f"game sprite: {prompt}",
            width=512,
            height=512,
            style=style
        )

        # Save original
        output_path = output_dir / f"{name}.png"
        image.save(output_path)
        print(f"Saved: {output_path}")

        # Also save resized version if needed
        if size != (512, 512):
            from PIL import Image as PILImage
            import io

            pil_image = PILImage.open(io.BytesIO(image.image_data))
            pil_image = pil_image.resize(size, PILImage.Resampling.NEAREST)

            small_path = output_dir / f"{name}_{size[0]}x{size[1]}.png"
            pil_image.save(small_path)
            print(f"Saved resized: {small_path}")

    elif asset_type == 'background':
        # Generate background
        output_dir = Path('assets/backgrounds')
        output_dir.mkdir(parents=True, exist_ok=True)

        image = await service.generate(
            prompt=f"game background: {prompt}",
            width=size[0] if size[0] > 256 else 1024,
            height=size[1] if size[1] > 256 else 768,
            style=style
        )

        output_path = output_dir / f"{name}.png"
        image.save(output_path)
        print(f"Saved: {output_path}")

    else:
        # Generic image
        output_dir = Path('assets')
        output_dir.mkdir(parents=True, exist_ok=True)

        image = await service.generate(
            prompt=prompt,
            width=size[0],
            height=size[1],
            style=style
        )

        output_path = output_dir / f"{name}.png"
        image.save(output_path)
        print(f"Saved: {output_path}")

    print("Done!")
    return output_path


def parse_size(size_str: str) -> tuple:
    """Parse size string like '64x64' to tuple."""
    try:
        parts = size_str.lower().split('x')
        return (int(parts[0]), int(parts[1]))
    except (ValueError, IndexError):
        raise ValueError(f"Invalid size format: {size_str}. Use WxH format (e.g., 64x64)")


def main():
    parser = argparse.ArgumentParser(
        description='Generate game assets using AI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s sprite "cute pixel art slime monster" slime_idle
  %(prog)s background "fantasy village at sunset" village_sunset
  %(prog)s sprite "dragon breathing fire" dragon_attack --size 128x128 --style cartoon
        """
    )

    parser.add_argument(
        'type',
        choices=['sprite', 'background', 'image'],
        help='Type of asset to generate'
    )
    parser.add_argument(
        'prompt',
        help='Description of the image to generate'
    )
    parser.add_argument(
        'name',
        help='Name for the output file (without extension)'
    )
    parser.add_argument(
        '--size', '-s',
        default='64x64',
        help='Output size in WxH format (default: 64x64 for sprites, 1024x768 for backgrounds)'
    )
    parser.add_argument(
        '--style',
        choices=['pixel_art', 'cartoon', 'realistic', 'sketch', 'sprite'],
        default='pixel_art',
        help='Art style (default: pixel_art)'
    )

    args = parser.parse_args()

    # Parse size
    size = parse_size(args.size)

    # Check environment
    vercel_url = os.getenv('VERCEL_APP_URL', '')
    api_key = os.getenv('GEMINI_API_KEY', '')
    use_mock = os.getenv('USE_MOCK_GENERATOR', '').lower() in ('true', '1', 'yes')

    if not vercel_url and not api_key and not use_mock:
        print("Warning: No VERCEL_APP_URL or GEMINI_API_KEY set.")
        print("Using mock generator (placeholder images).")
        print("")
        print("To use real image generation, set one of:")
        print("  export VERCEL_APP_URL=https://your-app.vercel.app")
        print("  export GEMINI_API_KEY=your_api_key")
        print("")

    # Run generation
    try:
        asyncio.run(generate_asset(
            asset_type=args.type,
            prompt=args.prompt,
            name=args.name,
            size=size,
            style=args.style
        ))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

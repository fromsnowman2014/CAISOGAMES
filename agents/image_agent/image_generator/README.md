# CAISOGAMES Image Generator

AI-powered image generation system for creating game assets. Uses Google's Gemini API to generate sprites, backgrounds, and animations.

## Features

- **AI Image Generation**: Generate game assets from text prompts using Gemini API
- **Sprite Processing**: Automatic background removal, pixelation, and color reduction
- **Format Conversion**: Support for PNG, JPG, GIF, and WebP formats
- **Animation Support**: Create animated GIFs from multiple frames
- **Caching**: Reduce API costs with intelligent caching
- **CLI Interface**: Easy-to-use command line tools

## Installation

```bash
cd image_generator
pip install -r requirements.txt
```

## Configuration

The generator reads the API key from environment variables:

```bash
# Set via environment variable
export GEMINI_API_KEY=your_api_key_here

# Or create a .env file (not committed to git)
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

For Vercel deployment, set `GEMINI_API_KEY` in the Vercel project settings.

## Usage

### CLI Commands

```bash
# Generate an image
python -m image_generator generate "pixel art dragon character" -o dragon.png

# Generate a sprite with processing
python -m image_generator sprite "cute slime monster" slime --size 64x64

# Create animation from frames
python -m image_generator animate frame1.png frame2.png frame3.png -o walk.gif

# Convert image format
python -m image_generator convert input.png output.jpg

# Check configuration
python -m image_generator check-config

# View cache statistics
python -m image_generator cache-stats
```

### Python API

```python
import asyncio
from image_generator import ImageGeneratorService

async def main():
    service = ImageGeneratorService()

    # Generate a sprite
    sprite_path = await service.generate_sprite(
        prompt="cute pixel art cat",
        name="cat_idle",
        size=(64, 64),
        pixelate=True,
        num_colors=16
    )
    print(f"Sprite saved to: {sprite_path}")

    # Generate a background
    bg_path = await service.generate_background(
        prompt="fantasy forest with mushrooms",
        name="forest_day",
        size=(800, 600)
    )
    print(f"Background saved to: {bg_path}")

asyncio.run(main())
```

### Quick Generation

```python
import asyncio
from image_generator import generate_image

async def main():
    data = await generate_image(
        "pixel art treasure chest",
        output_path="chest.png",
        width=256,
        height=256,
        style="pixel_art"
    )

asyncio.run(main())
```

## Project Structure

```
image_generator/
├── __init__.py          # Package exports
├── config.py            # Configuration management
├── main.py              # Main service class
├── cli.py               # Command-line interface
├── generators/
│   ├── base.py          # Abstract base generator
│   └── gemini_generator.py  # Gemini API implementation
├── processors/
│   ├── image_processor.py   # Core image processing
│   ├── format_converter.py  # Format conversion
│   └── sprite_processor.py  # Sprite-specific processing
├── utils/
│   ├── cache.py         # Image caching
│   ├── retry.py         # Retry logic
│   └── logger.py        # Logging utilities
├── requirements.txt     # Python dependencies
└── .env.example         # Environment template
```

## Supported Styles

- `pixel_art` - Retro pixel art style (default)
- `cartoon` - Cartoon/comic style
- `realistic` - Photorealistic style
- `sketch` - Hand-drawn sketch style

## Image Processing Features

### Sprite Processing

- Background removal (white/light backgrounds)
- Pixelation effect for retro style
- Color palette reduction (4, 8, 16, 32 colors)
- Outline addition
- Auto-cropping to content

### Format Conversion

- PNG (with transparency)
- JPEG (with quality control)
- GIF (single or animated)
- WebP (with transparency)

### Animation

- Create GIF from multiple frames
- Configurable frame duration
- Loop control
- Sprite sheet generation

## Caching

Generated images are cached to reduce API costs:

- Default cache size: 500 MB
- Default TTL: 7 days
- Cache key based on prompt + parameters

```python
# View cache stats
service = ImageGeneratorService()
print(service.get_cache_stats())

# Clear cache
service.clear_cache()
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | (required) |
| `IMAGE_CACHE_DIR` | Cache directory path | `./cache` |
| `CACHE_MAX_SIZE_MB` | Maximum cache size | `500` |

## Error Handling

The generator includes automatic retry logic for transient failures:

- Rate limiting: Automatic backoff and retry
- Network errors: Exponential backoff (max 3 retries)
- Content filtering: Raises `ContentFilterError`

## Integration with CAISOGAMES

This generator is designed to work with the CAISOGAMES graphics pipeline:

1. Generate base assets with appropriate prompts
2. Process sprites with `SpriteProcessor`
3. Save to `assets/sprites/` or `assets/backgrounds/`
4. Follow naming convention: `{entity}_{state}_{frame}.png`

See `/CLAUDE.md` for full game development guidelines.

## External API Usage

To use this image generator from other games or applications (Unity, Godot, Web), see the [API Usage Guide](API_USAGE.md).

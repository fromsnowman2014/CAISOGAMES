# Image Generator System - Technical Specification

## Overview

The Image Generator System is a modular Python-based solution for generating game assets using AI image generation APIs. It provides a unified interface for generating sprites, backgrounds, and UI elements with support for multiple output formats.

## Architecture

```
image_generator/
├── __init__.py                 # Package initialization
├── config.py                   # Configuration and environment management
├── generators/
│   ├── __init__.py
│   ├── base.py                 # Abstract base generator class
│   ├── gemini_generator.py     # Google Gemini/Imagen implementation
│   └── fallback_generator.py   # Fallback/mock generator for testing
├── processors/
│   ├── __init__.py
│   ├── image_processor.py      # Image manipulation (resize, crop, etc.)
│   ├── format_converter.py     # Format conversion (PNG, JPG, GIF, WebP)
│   └── sprite_processor.py     # Sprite-specific processing
├── utils/
│   ├── __init__.py
│   ├── cache.py                # Caching system for generated images
│   ├── retry.py                # Retry logic with exponential backoff
│   └── logger.py               # Logging utilities
├── cli.py                      # Command-line interface
├── main.py                     # Main entry point
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
└── README.md                   # Usage documentation
```

## API Selection Strategy

### Primary: Google Gemini API (Imagen)
- **Model**: Imagen 3 / Gemini 2.0 Flash
- **Pricing**: ~$0.04 per image
- **Best for**: High-quality backgrounds, character concepts
- **Output**: 1024x1024, 2048x2048

### Why Gemini First?
1. User already has API key
2. Excellent text rendering (good for UI elements)
3. Consistent style output
4. Native Python SDK available

### Fallback Options (Future)
- Replicate (Flux models) - $0.04/image
- Stability AI (SDXL) - Free tier available

## Core Components

### 1. Generator Interface

```python
class BaseGenerator(ABC):
    """Abstract base class for image generators"""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        width: int = 1024,
        height: int = 1024,
        style: str = "default",
        num_images: int = 1
    ) -> List[GeneratedImage]:
        """Generate images from prompt"""
        pass
```

### 2. Generated Image Model

```python
@dataclass
class GeneratedImage:
    image_data: bytes           # Raw image bytes
    format: str                 # 'png', 'jpg', etc.
    width: int
    height: int
    prompt: str                 # Original prompt
    metadata: Dict[str, Any]    # Additional metadata
    timestamp: datetime
```

### 3. Prompt Templates for Game Assets

```python
PROMPT_TEMPLATES = {
    "sprite": "pixel art game sprite, {subject}, {action}, transparent background, 32x32 pixels, retro style, {additional}",
    "background": "game background, {scene}, {mood}, parallax layers, high detail, {additional}",
    "ui_element": "game UI element, {element}, clean design, vector style, {additional}",
    "character": "game character design, {character}, {pose}, full body, concept art style, {additional}",
}
```

## Security Architecture

### Environment Variables

```env
# .env (NEVER commit)
GEMINI_API_KEY=AIzaSy...
IMAGE_CACHE_DIR=./cache
LOG_LEVEL=INFO
MAX_RETRIES=3
RETRY_DELAY=1.0
```

### API Key Protection

1. **Backend Only**: API calls made server-side only
2. **Environment Variables**: Keys stored in `.env` file
3. **Git Ignored**: `.env` in `.gitignore`
4. **Validation**: Key format validation before use
5. **Rotation Support**: Easy key rotation via env var

### Rate Limiting

```python
class RateLimiter:
    """Prevent API abuse and manage quotas"""

    def __init__(self, max_requests: int = 50, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = []

    async def acquire(self):
        """Wait if rate limit exceeded"""
        pass
```

## Image Processing Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Prompt    │───►│  Generator  │───►│  Processor  │───►│   Output    │
│   Input     │    │  (Gemini)   │    │  (Pillow)   │    │   File      │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                          │                  │
                          ▼                  ▼
                   ┌─────────────┐    ┌─────────────┐
                   │    Cache    │    │   Format    │
                   │   (SQLite)  │    │  Converter  │
                   └─────────────┘    └─────────────┘
```

## CLI Interface

```bash
# Generate a sprite
python -m image_generator generate \
  --type sprite \
  --prompt "purple monster eating food" \
  --output ./assets/sprites/caiso_eat.png \
  --size 256x256

# Generate a background
python -m image_generator generate \
  --type background \
  --prompt "village at sunset, peaceful" \
  --output ./assets/backgrounds/village_sunset.png \
  --size 1920x1080

# Generate multiple variations
python -m image_generator generate \
  --prompt "villager character running" \
  --output ./assets/sprites/villager_run_{n}.png \
  --count 4

# Convert format
python -m image_generator convert \
  --input ./sprite.png \
  --output ./sprite.gif \
  --frames 4 \
  --delay 100
```

## Caching Strategy

### Cache Key Generation
```python
def generate_cache_key(prompt: str, params: dict) -> str:
    """Generate deterministic cache key"""
    data = f"{prompt}:{json.dumps(params, sort_keys=True)}"
    return hashlib.sha256(data.encode()).hexdigest()[:16]
```

### Cache Storage (SQLite)
```sql
CREATE TABLE image_cache (
    cache_key TEXT PRIMARY KEY,
    prompt TEXT,
    params TEXT,
    image_path TEXT,
    created_at TIMESTAMP,
    accessed_at TIMESTAMP,
    hit_count INTEGER DEFAULT 0
);
```

### Cache Policy
- **TTL**: 7 days
- **Max Size**: 500MB
- **Eviction**: LRU (Least Recently Used)

## Error Handling

### Retry Strategy
```python
@retry(
    max_attempts=3,
    delay=1.0,
    exponential_backoff=True,
    exceptions=(APIError, TimeoutError, ConnectionError)
)
async def generate_with_retry(prompt: str) -> GeneratedImage:
    pass
```

### Error Types
| Error | Action |
|-------|--------|
| Rate Limited | Wait and retry with backoff |
| Invalid Key | Fail fast, log error |
| Timeout | Retry up to 3 times |
| Content Filter | Return placeholder, log warning |
| Network Error | Retry with exponential backoff |

## Output Formats

### Supported Formats
| Format | Use Case | Compression |
|--------|----------|-------------|
| PNG | Sprites (transparency) | Lossless |
| JPG | Backgrounds | 85% quality |
| WebP | Web optimization | 90% quality |
| GIF | Animations | 256 colors max |

### Sprite Sheet Generation
```python
def create_sprite_sheet(
    sprites: List[Image],
    columns: int = 4,
    padding: int = 2
) -> Image:
    """Combine multiple sprites into a single sheet"""
    pass
```

## Integration with Game Development

### Workflow
1. **Claude Code** identifies need for asset
2. Calls `image_generator` with prompt
3. Generator creates image via Gemini API
4. Processor optimizes for game use
5. Output saved to `assets/` folder
6. Game code updated with new asset path

### Example Integration
```python
# In game development workflow
from image_generator import generate_asset

# Generate character sprite
result = await generate_asset(
    prompt="cute purple monster with horns, happy expression",
    asset_type="sprite",
    output_path="./assets/sprites/caiso_happy.png",
    size=(256, 256)
)

print(f"Asset saved: {result.path}")
```

## Performance Targets

| Metric | Target |
|--------|--------|
| Generation Time | < 10 seconds |
| Cache Hit Rate | > 60% |
| Success Rate | > 95% |
| Memory Usage | < 500MB |

## Dependencies

```txt
# requirements.txt
google-generativeai>=0.8.0
Pillow>=10.0.0
python-dotenv>=1.0.0
aiohttp>=3.9.0
aiofiles>=23.0.0
click>=8.1.0
rich>=13.0.0
```

## Future Enhancements

1. **Multi-Provider Support**: Add Replicate, Stability AI
2. **Style Transfer**: Apply consistent art style across assets
3. **Batch Processing**: Generate multiple assets in parallel
4. **Web UI**: Simple web interface for non-CLI users
5. **Asset Library**: Pre-generated common game assets
6. **LoRA Support**: Fine-tune on specific art styles

---
*Document Version: 1.0*
*Created: 2026-02-02*

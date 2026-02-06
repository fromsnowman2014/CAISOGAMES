"""
Configuration management for Image Generator.
Loads settings from environment variables.
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
try:
    from dotenv import load_dotenv
except ImportError:
    # dotenv not available, will rely on system env vars
    def load_dotenv(*args, **kwargs):
        pass


# Load .env file from the image_generator directory or parent
_env_paths = [
    Path(__file__).parent / '.env',
    Path(__file__).parent.parent / '.env',
]

for env_path in _env_paths:
    if env_path.exists():
        load_dotenv(env_path)
        break


@dataclass
class Config:
    """Application configuration loaded from environment variables."""

    # API Keys
    gemini_api_key: str = field(default_factory=lambda: os.getenv('GEMINI_API_KEY', ''))

    # Cache settings
    cache_dir: Path = field(default_factory=lambda: Path(os.getenv('IMAGE_CACHE_DIR', './cache')))
    cache_max_size_mb: int = field(default_factory=lambda: int(os.getenv('CACHE_MAX_SIZE_MB', '500')))
    cache_ttl_days: int = field(default_factory=lambda: int(os.getenv('CACHE_TTL_DAYS', '7')))

    # Logging
    log_level: str = field(default_factory=lambda: os.getenv('LOG_LEVEL', 'INFO'))

    # Rate limiting
    max_requests_per_minute: int = field(default_factory=lambda: int(os.getenv('MAX_REQUESTS_PER_MINUTE', '50')))

    # Retry settings
    max_retries: int = field(default_factory=lambda: int(os.getenv('MAX_RETRIES', '3')))
    retry_delay: float = field(default_factory=lambda: float(os.getenv('RETRY_DELAY', '1.0')))

    # Output settings
    default_output_dir: Path = field(default_factory=lambda: Path('./assets'))

    def validate(self) -> bool:
        """Validate configuration."""
        errors = []

        if not self.gemini_api_key:
            errors.append("GEMINI_API_KEY is required")

        if self.gemini_api_key and not self.gemini_api_key.startswith('AIza'):
            errors.append("GEMINI_API_KEY appears to be invalid (should start with 'AIza')")

        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")

        return True

    def ensure_directories(self):
        """Create necessary directories."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.default_output_dir.mkdir(parents=True, exist_ok=True)
        (self.default_output_dir / 'sprites').mkdir(exist_ok=True)
        (self.default_output_dir / 'backgrounds').mkdir(exist_ok=True)


# Global config instance
config = Config()


def load_config() -> Config:
    """Load and return a new Config instance."""
    return Config()


# Prompt templates for different asset types
PROMPT_TEMPLATES = {
    "sprite": (
        "Create a game sprite: {subject}. "
        "Style: clean vector art, suitable for 2D game, transparent background. "
        "View: {view}. Additional details: {additional}"
    ),
    "sprite_pixel": (
        "Create pixel art game sprite: {subject}. "
        "Style: 16-bit retro pixel art, limited color palette, transparent background. "
        "Size reference: 32x32 or 64x64 pixels. View: {view}. Additional: {additional}"
    ),
    "background": (
        "Create a game background scene: {scene}. "
        "Style: illustrated game art, suitable for parallax scrolling, vibrant colors. "
        "Mood: {mood}. Time of day: {time}. Additional: {additional}"
    ),
    "character": (
        "Create a game character design: {character}. "
        "Style: cute cartoon game character, full body, clear silhouette. "
        "Pose: {pose}. Expression: {expression}. Additional: {additional}"
    ),
    "ui_element": (
        "Create a game UI element: {element}. "
        "Style: modern game UI, clean design, suitable for mobile. "
        "Color scheme: {colors}. Additional: {additional}"
    ),
    "item": (
        "Create a game item/object: {item}. "
        "Style: game asset, clear and recognizable, suitable for inventory. "
        "Category: {category}. Additional: {additional}"
    ),
}


def get_prompt_template(asset_type: str) -> str:
    """Get prompt template for asset type."""
    return PROMPT_TEMPLATES.get(asset_type, PROMPT_TEMPLATES["sprite"])

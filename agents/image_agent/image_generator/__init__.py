"""
Image Generator Package for CAISOGAMES.

A modular system for generating game assets using AI image generation APIs.
Supports Gemini API with caching, format conversion, and sprite processing.
"""

from .config import Config, load_config, PROMPT_TEMPLATES
from .main import ImageGeneratorService, generate_image
from .generators.base import GeneratedImage, GeneratorError
from .generators.gemini_rest_generator import GeminiRestGenerator
from .processors.image_processor import ImageProcessor
from .processors.format_converter import FormatConverter
from .processors.sprite_processor import SpriteProcessor
from .utils.cache import ImageCache
from .utils.logger import setup_logging, get_logger

__version__ = "1.0.0"
__all__ = [
    # Config
    "Config",
    "load_config",
    "PROMPT_TEMPLATES",
    # Main service
    "ImageGeneratorService",
    "generate_image",
    # Generators
    "GeneratedImage",
    "GeneratorError",
    "GeminiRestGenerator",
    # Processors
    "ImageProcessor",
    "FormatConverter",
    "SpriteProcessor",
    # Utils
    "ImageCache",
    "setup_logging",
    "get_logger",
]

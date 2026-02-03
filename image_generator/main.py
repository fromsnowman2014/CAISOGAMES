"""Main entry point for image generator module."""

import os
import asyncio
from pathlib import Path
from typing import List, Optional, Dict, Any

from .config import Config, load_config
from .generators.base import GeneratedImage, GeneratorError
from .generators.gemini_rest_generator import GeminiRestGenerator
from .generators.mock_generator import MockGenerator
from .generators.vercel_proxy_generator import VercelProxyGenerator
from .processors.image_processor import ImageProcessor
from .processors.format_converter import FormatConverter
from .processors.sprite_processor import SpriteProcessor
from .utils.cache import ImageCache
from .utils.logger import setup_logging, get_logger, GenerationLogger


class ImageGeneratorService:
    """
    Main service for AI-powered game asset generation.

    Provides a high-level API for generating and processing game assets.
    Supports caching, multiple output formats, and sprite processing.

    Generator selection (in order of priority):
    1. USE_MOCK_GENERATOR=true -> MockGenerator (for testing)
    2. VERCEL_APP_URL set -> VercelProxyGenerator (for Claude Code development)
    3. GEMINI_API_KEY set -> GeminiRestGenerator (direct API access)
    4. None of above -> MockGenerator (fallback)
    """

    def __init__(
        self,
        config: Optional[Config] = None,
        use_mock: Optional[bool] = None,
        use_proxy: Optional[bool] = None
    ):
        """
        Initialize the image generator service.

        Args:
            config: Configuration object (loads from env if not provided)
            use_mock: Force mock mode (auto-detects from env if None)
            use_proxy: Force Vercel proxy mode (auto-detects from env if None)
        """
        self.config = config or load_config()

        # Determine generator mode
        if use_mock is None:
            use_mock = os.getenv('USE_MOCK_GENERATOR', '').lower() in ('true', '1', 'yes')

        if use_proxy is None:
            use_proxy = bool(os.getenv('VERCEL_APP_URL', ''))

        # Select generator based on configuration
        self._generator_type = 'unknown'

        if use_mock:
            self.generator = MockGenerator()
            self._generator_type = 'mock'
        elif use_proxy:
            vercel_url = os.getenv('VERCEL_APP_URL', '')
            self.generator = VercelProxyGenerator(vercel_url=vercel_url)
            self._generator_type = 'vercel-proxy'
        elif self.config.gemini_api_key:
            self.generator = GeminiRestGenerator(self.config.gemini_api_key)
            self._generator_type = 'gemini-rest'
        else:
            # Fallback to mock
            self.generator = MockGenerator()
            self._generator_type = 'mock'

        self.cache = ImageCache(
            self.config.cache_dir,
            max_size_mb=self.config.cache_max_size_mb
        )
        self.logger = GenerationLogger()

        setup_logging()

    @property
    def is_mock(self) -> bool:
        """Returns True if using mock generator."""
        return self._generator_type == 'mock'

    @property
    def generator_type(self) -> str:
        """Returns the type of generator being used."""
        return self._generator_type

    async def generate(
        self,
        prompt: str,
        width: int = 512,
        height: int = 512,
        style: str = 'pixel_art',
        use_cache: bool = True,
        **kwargs
    ) -> GeneratedImage:
        """
        Generate an image from a text prompt.

        Args:
            prompt: Description of the image to generate
            width: Image width in pixels
            height: Image height in pixels
            style: Art style (pixel_art, cartoon, realistic, sketch)
            use_cache: Whether to use caching
            **kwargs: Additional generator options

        Returns:
            GeneratedImage with the result
        """
        # Check cache
        cache_key = self.cache.generate_key(
            prompt=prompt,
            generator='gemini',
            width=width,
            height=height,
            style=style
        )

        if use_cache:
            cached = self.cache.get(cache_key)
            if cached:
                self.logger.cache_hit(cache_key)
                return GeneratedImage(
                    image_data=cached,
                    prompt=prompt,
                    width=width,
                    height=height,
                    format='png'
                )
            self.logger.cache_miss(cache_key)

        # Generate new image
        gen_id = self.logger.start_generation(prompt, 'gemini', width, height)

        import time
        start = time.time()

        try:
            images = await self.generator.generate(
                prompt=prompt,
                width=width,
                height=height,
                style=style,
                **kwargs
            )

            if not images:
                raise GeneratorError("No images generated")

            image = images[0]
            duration = time.time() - start
            self.logger.generation_success(gen_id, duration)

            # Cache the result
            if use_cache:
                self.cache.put(
                    key=cache_key,
                    data=image.image_data,
                    prompt=prompt,
                    generator='gemini',
                    width=width,
                    height=height,
                    metadata={'style': style}
                )

            return image

        except Exception as e:
            self.logger.generation_failed(gen_id, e)
            raise

    async def generate_sprite(
        self,
        prompt: str,
        name: str,
        size: tuple = (64, 64),
        output_dir: str = './assets/sprites',
        pixelate: bool = True,
        num_colors: int = 16,
        add_outline: bool = False
    ) -> Path:
        """
        Generate and process a game sprite.

        Args:
            prompt: Description of the sprite
            name: Name for the sprite file
            size: Target size (width, height)
            output_dir: Directory to save sprite
            pixelate: Apply pixel art effect
            num_colors: Colors in palette
            add_outline: Add outline to sprite

        Returns:
            Path to saved sprite
        """
        # Generate at higher resolution
        image = await self.generate(
            prompt=f"game sprite character: {prompt}",
            width=512,
            height=512,
            style='pixel_art'
        )

        # Process as sprite
        processor = SpriteProcessor(output_dir)

        from PIL import Image as PILImage
        import io
        pil_image = PILImage.open(io.BytesIO(image.image_data))

        return processor.process_sprite(
            pil_image,
            name=name,
            size=size,
            remove_bg=True,
            pixelate=pixelate,
            pixel_size=max(1, 512 // size[0]),
            reduce_colors=True,
            num_colors=num_colors,
            add_outline=add_outline
        )

    async def generate_background(
        self,
        prompt: str,
        name: str,
        size: tuple = (800, 600),
        output_dir: str = './assets/backgrounds'
    ) -> Path:
        """
        Generate a game background.

        Args:
            prompt: Description of the background
            name: Name for the background file
            size: Target size (width, height)
            output_dir: Directory to save background

        Returns:
            Path to saved background
        """
        image = await self.generate(
            prompt=f"game background scene: {prompt}",
            width=size[0],
            height=size[1],
            style='pixel_art'
        )

        output_path = Path(output_dir) / f"{name}.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(image.image_data)

        return output_path

    async def generate_animation_frames(
        self,
        base_prompt: str,
        frame_descriptions: List[str],
        name: str,
        frame_size: tuple = (64, 64),
        output_dir: str = './assets/sprites'
    ) -> Path:
        """
        Generate animation frames and create a GIF.

        Args:
            base_prompt: Base description for the character
            frame_descriptions: List of action descriptions for each frame
            name: Name for the animation
            frame_size: Size of each frame
            output_dir: Directory to save animation

        Returns:
            Path to saved GIF
        """
        frames = []
        processor = SpriteProcessor(output_dir)

        for i, desc in enumerate(frame_descriptions):
            prompt = f"{base_prompt}, {desc}"
            image = await self.generate(
                prompt=prompt,
                width=512,
                height=512,
                style='pixel_art'
            )

            from PIL import Image as PILImage
            import io
            pil_image = PILImage.open(io.BytesIO(image.image_data))

            # Process frame
            processed = ImageProcessor.remove_background(pil_image)
            processed = ImageProcessor.pixelate(processed, max(1, 512 // frame_size[0]))
            processed = ImageProcessor.reduce_colors(processed, 16)
            processed = ImageProcessor.resize(processed, frame_size)

            frames.append(processed)

        # Create animation
        return processor.create_animation(frames, name, frame_duration=150)

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return self.cache.get_stats()

    def clear_cache(self) -> int:
        """Clear the cache. Returns number of entries cleared."""
        return self.cache.clear()


# Convenience function for quick generation
async def generate_image(
    prompt: str,
    output_path: Optional[str] = None,
    **kwargs
) -> bytes:
    """
    Quick function to generate an image.

    Args:
        prompt: Image description
        output_path: Optional path to save the image
        **kwargs: Additional options passed to generate()

    Returns:
        Image data as bytes
    """
    service = ImageGeneratorService()
    image = await service.generate(prompt, **kwargs)

    if output_path:
        Path(output_path).write_bytes(image.image_data)

    return image.image_data


# Make CLI available when run as module
if __name__ == '__main__':
    from .cli import main
    main()

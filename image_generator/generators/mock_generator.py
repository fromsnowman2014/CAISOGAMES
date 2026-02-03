"""
Mock Generator for local testing without API access.
Generates placeholder images for development purposes.
"""

from typing import List
from PIL import Image, ImageDraw, ImageFont
import io

from .base import (
    BaseGenerator,
    GeneratedImage,
)


class MockGenerator(BaseGenerator):
    """
    Mock image generator for local testing.
    Generates placeholder images with prompt text.
    """

    SUPPORTED_SIZES = [
        (256, 256), (512, 512), (1024, 1024),
        (1024, 768), (768, 1024),
    ]

    def __init__(self, api_key: str = "mock"):
        """Initialize mock generator (api_key is ignored)."""
        self.api_key = api_key or "mock"

    @property
    def name(self) -> str:
        """Generator name for logging."""
        return "mock"

    @property
    def supported_sizes(self) -> List[tuple]:
        """List of supported (width, height) tuples."""
        return self.SUPPORTED_SIZES

    async def check_health(self) -> bool:
        """Always returns True for mock generator."""
        return True

    async def generate(
        self,
        prompt: str,
        width: int = 512,
        height: int = 512,
        num_images: int = 1,
        style: str = 'pixel_art',
        **kwargs
    ) -> List[GeneratedImage]:
        """
        Generate mock placeholder images.

        Creates colored placeholder images with the prompt text
        for testing the image pipeline without API access.
        """
        images = []

        # Style-based colors
        style_colors = {
            'pixel_art': (76, 175, 80),      # Green
            'cartoon': (255, 152, 0),         # Orange
            'realistic': (33, 150, 243),      # Blue
            'sketch': (158, 158, 158),        # Gray
        }
        bg_color = style_colors.get(style, (100, 100, 100))

        for i in range(num_images):
            # Create image
            img = Image.new('RGBA', (width, height), bg_color + (255,))
            draw = ImageDraw.Draw(img)

            # Add border
            border_color = (255, 255, 255, 180)
            draw.rectangle([10, 10, width-10, height-10], outline=border_color, width=3)

            # Add text
            text_color = (255, 255, 255)

            # Title
            title = f"[MOCK] {style.upper()}"
            draw.text((width//2, 30), title, fill=text_color, anchor="mt")

            # Prompt (wrapped)
            prompt_lines = self._wrap_text(prompt, width - 40)
            y_pos = height // 3
            for line in prompt_lines[:5]:  # Max 5 lines
                draw.text((width//2, y_pos), line, fill=text_color, anchor="mt")
                y_pos += 20

            # Size info
            size_text = f"{width}x{height}"
            draw.text((width//2, height - 30), size_text, fill=text_color, anchor="mb")

            # Convert to bytes
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            image_data = buffer.getvalue()

            images.append(GeneratedImage(
                image_data=image_data,
                prompt=prompt,
                width=width,
                height=height,
                format='png'
            ))

        return images

    def _wrap_text(self, text: str, max_width: int) -> List[str]:
        """Simple text wrapping."""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        chars_per_line = max_width // 8  # Approximate chars per line

        for word in words:
            if current_length + len(word) + 1 <= chars_per_line:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)

        if current_line:
            lines.append(' '.join(current_line))

        return lines

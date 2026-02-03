"""Core image processing utilities."""

from pathlib import Path
from typing import Tuple, Optional, Union
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import io


class ImageProcessor:
    """Handles common image processing operations for game assets."""

    @staticmethod
    def resize(
        image: Image.Image,
        size: Tuple[int, int],
        maintain_aspect: bool = True,
        resample: int = Image.Resampling.LANCZOS
    ) -> Image.Image:
        """
        Resize an image to the specified dimensions.

        Args:
            image: PIL Image to resize
            size: Target (width, height)
            maintain_aspect: If True, maintains aspect ratio with padding
            resample: Resampling filter to use

        Returns:
            Resized PIL Image
        """
        if maintain_aspect:
            image.thumbnail(size, resample)
            # Create new image with target size and paste centered
            new_image = Image.new('RGBA', size, (0, 0, 0, 0))
            paste_x = (size[0] - image.width) // 2
            paste_y = (size[1] - image.height) // 2
            new_image.paste(image, (paste_x, paste_y))
            return new_image
        else:
            return image.resize(size, resample)

    @staticmethod
    def remove_background(
        image: Image.Image,
        threshold: int = 240,
        tolerance: int = 10
    ) -> Image.Image:
        """
        Remove white/light background from an image.

        Args:
            image: PIL Image
            threshold: Brightness threshold for background detection
            tolerance: Color tolerance for edge detection

        Returns:
            Image with transparent background
        """
        # Convert to RGBA if needed
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        data = image.getdata()
        new_data = []

        for item in data:
            # Check if pixel is close to white
            if item[0] > threshold and item[1] > threshold and item[2] > threshold:
                new_data.append((255, 255, 255, 0))  # Make transparent
            else:
                new_data.append(item)

        image.putdata(new_data)
        return image

    @staticmethod
    def crop_to_content(
        image: Image.Image,
        padding: int = 0
    ) -> Image.Image:
        """
        Crop image to non-transparent content.

        Args:
            image: PIL Image with transparency
            padding: Pixels of padding around content

        Returns:
            Cropped image
        """
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        # Get bounding box of non-transparent pixels
        bbox = image.getbbox()

        if bbox:
            # Add padding
            left = max(0, bbox[0] - padding)
            top = max(0, bbox[1] - padding)
            right = min(image.width, bbox[2] + padding)
            bottom = min(image.height, bbox[3] + padding)

            return image.crop((left, top, right, bottom))

        return image

    @staticmethod
    def add_outline(
        image: Image.Image,
        color: Tuple[int, int, int, int] = (0, 0, 0, 255),
        thickness: int = 2
    ) -> Image.Image:
        """
        Add an outline around non-transparent pixels.

        Args:
            image: PIL Image with transparency
            color: RGBA color for outline
            thickness: Outline thickness in pixels

        Returns:
            Image with outline
        """
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        # Create outline by dilating alpha channel
        alpha = image.split()[3]

        # Dilate the alpha channel
        for _ in range(thickness):
            alpha = alpha.filter(ImageFilter.MaxFilter(3))

        # Create outline image
        outline = Image.new('RGBA', image.size, color)
        outline.putalpha(alpha)

        # Composite original over outline
        outline.paste(image, (0, 0), image)

        return outline

    @staticmethod
    def pixelate(
        image: Image.Image,
        pixel_size: int = 8
    ) -> Image.Image:
        """
        Apply pixelation effect for retro game style.

        Args:
            image: PIL Image
            pixel_size: Size of each "pixel" block

        Returns:
            Pixelated image
        """
        # Downscale
        small = image.resize(
            (image.width // pixel_size, image.height // pixel_size),
            resample=Image.Resampling.NEAREST
        )

        # Upscale back with nearest neighbor
        return small.resize(image.size, resample=Image.Resampling.NEAREST)

    @staticmethod
    def reduce_colors(
        image: Image.Image,
        num_colors: int = 16
    ) -> Image.Image:
        """
        Reduce color palette for retro game style.

        Args:
            image: PIL Image
            num_colors: Number of colors in palette

        Returns:
            Image with reduced color palette
        """
        # Preserve alpha if present
        if image.mode == 'RGBA':
            alpha = image.split()[3]
            rgb = image.convert('RGB')
            quantized = rgb.quantize(colors=num_colors).convert('RGB')
            result = quantized.convert('RGBA')
            result.putalpha(alpha)
            return result
        else:
            return image.quantize(colors=num_colors).convert('RGB')

    @staticmethod
    def adjust_brightness(
        image: Image.Image,
        factor: float = 1.0
    ) -> Image.Image:
        """
        Adjust image brightness.

        Args:
            image: PIL Image
            factor: Brightness factor (1.0 = original, >1 = brighter, <1 = darker)

        Returns:
            Adjusted image
        """
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)

    @staticmethod
    def adjust_contrast(
        image: Image.Image,
        factor: float = 1.0
    ) -> Image.Image:
        """
        Adjust image contrast.

        Args:
            image: PIL Image
            factor: Contrast factor (1.0 = original)

        Returns:
            Adjusted image
        """
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)

    @staticmethod
    def to_bytes(
        image: Image.Image,
        format: str = 'PNG'
    ) -> bytes:
        """
        Convert PIL Image to bytes.

        Args:
            image: PIL Image
            format: Output format

        Returns:
            Image as bytes
        """
        buffer = io.BytesIO()
        image.save(buffer, format=format)
        return buffer.getvalue()

    @staticmethod
    def from_bytes(data: bytes) -> Image.Image:
        """
        Create PIL Image from bytes.

        Args:
            data: Image data as bytes

        Returns:
            PIL Image
        """
        return Image.open(io.BytesIO(data))
